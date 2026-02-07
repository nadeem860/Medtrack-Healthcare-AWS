#!/usr/bin/env python3
"""
Script to create DynamoDB tables for MedTrack application
Run this before deploying to AWS
"""

import boto3
from botocore.exceptions import ClientError
import sys

# Configuration
REGION = 'us-east-1'  # Change to your preferred region
dynamodb = boto3.client('dynamodb', region_name=REGION)

def create_users_table():
    """Create Users table with email as partition key"""
    try:
        response = dynamodb.create_table(
            TableName='MedTrack_Users',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'UserIdIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("✅ Users table created successfully")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️  Users table already exists")
            return True
        else:
            print(f"❌ Error creating Users table: {e}")
            return False

def create_appointments_table():
    """Create Appointments table with appointment_id as partition key"""
    try:
        response = dynamodb.create_table(
            TableName='MedTrack_Appointments',
            KeySchema=[
                {
                    'AttributeName': 'appointment_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'appointment_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'patient_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'PatientIdIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'patient_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("✅ Appointments table created successfully")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️  Appointments table already exists")
            return True
        else:
            print(f"❌ Error creating Appointments table: {e}")
            return False

def create_medical_records_table():
    """Create Medical Records table with record_id as partition key"""
    try:
        response = dynamodb.create_table(
            TableName='MedTrack_MedicalRecords',
            KeySchema=[
                {
                    'AttributeName': 'record_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'record_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'patient_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'PatientIdIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'patient_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("✅ Medical Records table created successfully")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️  Medical Records table already exists")
            return True
        else:
            print(f"❌ Error creating Medical Records table: {e}")
            return False

def wait_for_tables():
    """Wait for all tables to become active"""
    print("\n⏳ Waiting for tables to become active...")
    tables = ['MedTrack_Users', 'MedTrack_Appointments', 'MedTrack_MedicalRecords']
    
    for table_name in tables:
        try:
            waiter = dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=table_name)
            print(f"✅ {table_name} is active")
        except ClientError as e:
            print(f"❌ Error waiting for {table_name}: {e}")

def main():
    print("=" * 60)
    print("🏥 MedTrack DynamoDB Table Creation")
    print("=" * 60)
    print(f"Region: {REGION}")
    print()
    
    # Check AWS credentials
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"AWS Account: {identity['Account']}")
        print(f"User ARN: {identity['Arn']}")
        print()
    except ClientError as e:
        print("❌ AWS credentials not configured properly")
        print("Run: aws configure")
        sys.exit(1)
    
    # Create tables
    print("Creating DynamoDB tables...")
    print()
    
    success = True
    success &= create_users_table()
    success &= create_appointments_table()
    success &= create_medical_records_table()
    
    if success:
        wait_for_tables()
        print()
        print("=" * 60)
        print("✅ All tables created successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Set environment variables:")
        print("   export USE_AWS=true")
        print("   export AWS_REGION=us-east-1")
        print("   export SECRET_KEY='your-secure-key'")
        print()
        print("2. (Optional) Create SNS topic for notifications:")
        print("   aws sns create-topic --name MedTrack-Notifications")
        print("   export SNS_TOPIC_ARN='arn:aws:sns:...'")
        print()
        print("3. Run the application:")
        print("   python aws_app.py")
        print()
    else:
        print()
        print("❌ Some tables failed to create. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
