from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid
from datetime import datetime
import os

app = Flask(__name__)
# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Helper function to generate unique IDs
def generate_id():
    return str(uuid.uuid4())

# In-memory data storage (Phase 1)
users = {}  # Will store both patients and doctors
appointments = {}
medical_records = {}

# Demo data for testing
def initialize_demo_data():
    """Initialize some demo data for testing purposes"""
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
        'created_at': datetime.now(),
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
        'created_at': datetime.now(),
        'appointments': [],
        'patients': []
    }
    users[doctor_id] = demo_doctor

# Initialize demo data when the app starts
initialize_demo_data()

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
        
        # Check if user exists and password matches
        for user_id, user in users.items():
            if user['email'] == email and user['password'] == password:
                session['user_id'] = user_id
                session['user_type'] = user['user_type']
                session['user_name'] = f"{user['first_name']} {user['last_name']}"
                
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
        for user in users.values():
            if user['email'] == email:
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
            'created_at': datetime.now(),
            'appointments': [],
            'medical_history': []
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
            new_user['patients'] = []
        
        users[user_id] = new_user
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Patient dashboard
@app.route('/home1')
def patient_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'patient':
        return redirect(url_for('login'))
    
    user = users[session['user_id']]
    return render_template('patient_dashboard.html', user=user)

# Doctor dashboard
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'doctor':
        return redirect(url_for('login'))
    
    user = users[session['user_id']]
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('booking.html')

# Ticket booking submission
@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Handle appointment booking
            appointment_id = generate_id()
            new_appointment = {
                'appointment_id': appointment_id,
                'patient_id': session['user_id'],
                'doctor_name': request.form['doctor'],
                'appointment_date': request.form['date'],
                'appointment_time': request.form['time'],
                'appointment_type': request.form.get('appointment_type', 'consultation'),
                'reason': request.form['reason'],
                'additional_notes': request.form.get('additional_notes', ''),
                'emergency_contact_name': request.form.get('emergency_contact_name', ''),
                'emergency_contact_phone': request.form.get('emergency_contact_phone', ''),
                'status': 'scheduled',
                'created_at': datetime.now()
            }
            
            appointments[appointment_id] = new_appointment
            users[session['user_id']]['appointments'].append(appointment_id)
            
            flash('Appointment booked successfully!', 'success')
            return render_template('tickets.html', appointment=new_appointment)
        except Exception as e:
            flash(f'Error booking appointment: {str(e)}', 'error')
            return redirect(url_for('booking'))
    
    return render_template('tickets.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Get debug mode from environment (disable in production)
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )