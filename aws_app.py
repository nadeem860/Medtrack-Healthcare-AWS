from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import uuid
from datetime import datetime
import os

app = Flask(__name__)
# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'aws-secret-key-change-in-production')

# -------------------------------------------------
# AWS CONFIG
# -------------------------------------------------
REGION = os.environ.get('AWS_REGION', 'us-east-1')
USE_AWS = os.environ.get('USE_AWS', 'false').lower() == 'true'

# Initialize AWS services only if USE_AWS is enabled
if USE_AWS:
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    sns = boto3.client("sns", region_name=REGION)
    
    # DynamoDB Tables (must exist in AWS)
    users_table = dynamodb.Table(os.environ.get('USERS_TABLE', 'MedTrack_Users'))
    appointments_table = dynamodb.Table(os.environ.get('APPOINTMENTS_TABLE', 'MedTrack_Appointments'))
    medical_records_table = dynamodb.Table(os.environ.get('RECORDS_TABLE', 'MedTrack_MedicalRecords'))
    
    # SNS Topic ARN (optional)
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
else:
    # Fallback to in-memory storage for local development
    users = {}
    appointments = {}
    medical_records = {}

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def generate_id():
    return str(uuid.uuid4())

def send_notification(subject, message):
    """Send SNS notification if AWS is enabled"""
    if not USE_AWS or not SNS_TOPIC_ARN:
        print(f"[NOTIFICATION] {subject}: {message}")
        return
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except ClientError as e:
        print(f"SNS Error: {e}")

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session

def get_user_by_email(email):
    """Get user by email from DynamoDB or in-memory storage"""
    if USE_AWS:
        try:
            # DynamoDB: email is the partition key
            response = users_table.get_item(Key={'email': email})
            return response.get('Item')
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            return None
    else:
        # In-memory: search through users
        for user_id, user in users.items():
            if user['email'] == email:
                return user
        return None

def create_user(user_data):
    """Create user in DynamoDB or in-memory storage"""
    if USE_AWS:
        try:
            users_table.put_item(Item=user_data)
            return True
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            return False
    else:
        users[user_data['user_id']] = user_data
        return True

def get_user_appointments(user_id):
    """Get all appointments for a user"""
    if USE_AWS:
        try:
            # Scan and filter (or use GSI if configured)
            response = appointments_table.scan()
            user_appointments = [
                item for item in response.get('Items', [])
                if item.get('patient_id') == user_id
            ]
            return user_appointments
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            return []
    else:
        # In-memory: get appointment IDs from user and fetch appointments
        user = users.get(user_id, {})
        appointment_ids = user.get('appointments', [])
        return [appointments[aid] for aid in appointment_ids if aid in appointments]

def create_appointment(appointment_data):
    """Create appointment in DynamoDB or in-memory storage"""
    if USE_AWS:
        try:
            appointments_table.put_item(Item=appointment_data)
            return True
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            return False
    else:
        appointment_id = appointment_data['appointment_id']
        appointments[appointment_id] = appointment_data
        # Add to user's appointment list
        patient_id = appointment_data['patient_id']
        if patient_id in users:
            users[patient_id]['appointments'].append(appointment_id)
        return True

def delete_appointment(appointment_id):
    """Delete appointment from DynamoDB or in-memory storage"""
    if USE_AWS:
        try:
            appointments_table.delete_item(Key={'appointment_id': appointment_id})
            return True
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            return False
    else:
        if appointment_id in appointments:
            # Remove from user's appointment list
            appointment = appointments[appointment_id]
            patient_id = appointment.get('patient_id')
            if patient_id in users:
                users[patient_id]['appointments'].remove(appointment_id)
            del appointments[appointment_id]
        return True

# -------------------------------------------------
# DEMO DATA (for local development only)
# -------------------------------------------------
def initialize_demo_data():
    """Initialize demo data for testing (only in non-AWS mode)"""
    if USE_AWS:
        return
    
    # Demo patient
    patient_id = generate_id()
    demo_patient = {
        'user_id': patient_id,
        'email': 'patient@demo.com',
        'password': 'password123',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone': '(555) 123-4567',
        'user_type': 'patient',
        'address': '123 Main St, City, State 12345',
        'date_of_birth': '1990-01-15',
        'emergency_contact': '(555) 987-6543',
        'created_at': datetime.now().isoformat(),
        'appointments': [],
        'medical_history': []
    }
    users[patient_id] = demo_patient
    
    # Demo doctor
    doctor_id = generate_id()
    demo_doctor = {
        'user_id': doctor_id,
        'email': 'doctor@demo.com',
        'password': 'password123',
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'phone': '(555) 456-7890',
        'user_type': 'doctor',
        'specialization': 'General Medicine',
        'license_number': 'MD123456',
        'office_address': '456 Medical Center Dr, City, State 12345',
        'created_at': datetime.now().isoformat(),
        'appointments': [],
        'patients': []
    }
    users[doctor_id] = demo_doctor

# Initialize demo data when the app starts (only for local mode)
if not USE_AWS:
    initialize_demo_data()

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

# Home/Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Get user from database
        user = get_user_by_email(email)
        
        if user and user['password'] == password:
            # Set session
            session.clear()
            session['user_id'] = user['user_id']
            session['user_type'] = user['user_type']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            session['user_email'] = user['email']
            
            # Send notification
            send_notification(
                "User Login",
                f"{email} logged in at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            # Redirect based on user type
            if user['user_type'] == 'patient':
                return redirect(url_for('patient_dashboard'))
            else:
                return redirect(url_for('doctor_dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_type = request.form['user_type']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        
        # Check if email already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        # Create new user
        user_id = generate_id()
        new_user = {
            'user_id': user_id,
            'email': email,
            'password': password,  # In production, this should be hashed
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'user_type': user_type,
            'created_at': datetime.now().isoformat(),
            'appointments': [] if not USE_AWS else None,  # DynamoDB doesn't need empty lists
            'medical_history': [] if not USE_AWS else None
        }
        
        # Add user-type specific fields
        if user_type == 'patient':
            new_user['address'] = request.form.get('address', '')
            new_user['date_of_birth'] = request.form.get('date_of_birth', '')
            new_user['emergency_contact'] = request.form.get('emergency_contact', '')
        else:  # doctor
            new_user['specialization'] = request.form.get('specialization', '')
            new_user['license_number'] = request.form.get('license_number', '')
            new_user['office_address'] = request.form.get('office_address', '')
            if not USE_AWS:
                new_user['patients'] = []
        
        # Save user
        if create_user(new_user):
            # Send notification
            send_notification(
                "New User Registered",
                f"{email} ({user_type}) registered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('signup.html')

# Patient dashboard
@app.route('/home1')
def patient_dashboard():
    if not is_logged_in() or session.get('user_type') != 'patient':
        return redirect(url_for('login'))
    
    # Get user data
    if USE_AWS:
        user = get_user_by_email(session['user_email'])
    else:
        user = users.get(session['user_id'])
    
    # Get user appointments
    user_appointments = get_user_appointments(session['user_id'])
    
    return render_template('patient_dashboard.html', user=user, appointments=user_appointments)

# Doctor dashboard
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if not is_logged_in() or session.get('user_type') != 'doctor':
        return redirect(url_for('login'))
    
    # Get user data
    if USE_AWS:
        user = get_user_by_email(session['user_email'])
    else:
        user = users.get(session['user_id'])
    
    return render_template('doctor_dashboard.html', user=user)

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact_us')
def contact_us():
    return render_template('contact.html')

# Booking page
@app.route('/booking')
@app.route('/b1')  # Keep backward compatibility
def booking():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('booking.html')

# Ticket booking submission
@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Handle appointment booking
            appointment_id = generate_id()
            new_appointment = {
                'appointment_id': appointment_id,
                'patient_id': session['user_id'],
                'patient_name': session['user_name'],
                'patient_email': session['user_email'],
                'doctor_name': request.form['doctor'],
                'appointment_date': request.form['date'],
                'appointment_time': request.form['time'],
                'appointment_type': request.form.get('appointment_type', 'consultation'),
                'reason': request.form['reason'],
                'additional_notes': request.form.get('additional_notes', ''),
                'emergency_contact_name': request.form.get('emergency_contact_name', ''),
                'emergency_contact_phone': request.form.get('emergency_contact_phone', ''),
                'status': 'scheduled',
                'created_at': datetime.now().isoformat()
            }
            
            # Save appointment
            if create_appointment(new_appointment):
                # Send notification
                send_notification(
                    "New Appointment Booked",
                    f"{session['user_email']} booked appointment with {new_appointment['doctor_name']} on {new_appointment['appointment_date']} at {new_appointment['appointment_time']}"
                )
                flash('Appointment booked successfully!', 'success')
                return render_template('tickets.html', appointment=new_appointment)
            else:
                flash('Failed to book appointment. Please try again.', 'error')
                return redirect(url_for('booking'))
        except Exception as e:
            flash(f'Error booking appointment: {str(e)}', 'error')
            return redirect(url_for('booking'))
    
    return render_template('tickets.html')

# View all appointments (for patients)
@app.route('/appointments')
def appointments():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    # Get user appointments
    user_appointments = get_user_appointments(session['user_id'])
    
    return render_template('appointments.html', appointments=user_appointments)

# Cancel appointment
@app.route('/appointments/cancel/<appointment_id>')
def cancel_appointment(appointment_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    if delete_appointment(appointment_id):
        send_notification(
            "Appointment Cancelled",
            f"{session['user_email']} cancelled appointment {appointment_id}"
        )
        flash('Appointment cancelled successfully', 'success')
    else:
        flash('Failed to cancel appointment', 'error')
    
    return redirect(url_for('appointments'))

# Logout
@app.route('/logout')
def logout():
    user_email = session.get('user_email', 'Unknown')
    session.clear()
    send_notification("User Logout", f"{user_email} logged out")
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Get debug mode from environment (disable in production)
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("=" * 50)
    print("🏥 MedTrack Healthcare Management System")
    print("=" * 50)
    print(f"Mode: {'AWS (DynamoDB + SNS)' if USE_AWS else 'Local (In-Memory)'}")
    print(f"Region: {REGION}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("=" * 50)
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )
