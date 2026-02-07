# AWS Setup Guide

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Python 3.7+

## Step 1: Configure AWS CLI

```bash
aws configure
```

Enter your AWS Access Key ID, Secret Access Key, and region (us-east-1).

## Step 2: Create DynamoDB Tables

```bash
python create_dynamodb_tables.py
```

This creates:
- MedTrack_Users
- MedTrack_Appointments
- MedTrack_MedicalRecords

## Step 3: Create SNS Topic (Optional)

```bash
aws sns create-topic --name MedTrack-Notifications
```

Save the Topic ARN for environment variables.

## Step 4: Deploy to Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.8 medtrack-app --region us-east-1

# Create environment
eb create medtrack-env

# Open in browser
eb open
```

## Step 5: Set Environment Variables in EB

```bash
eb setenv USE_AWS=true AWS_REGION=us-east-1 SECRET_KEY='your-key' SNS_TOPIC_ARN='your-arn'
```

## IAM Permissions Required

Your EB environment needs:
- DynamoDB: PutItem, GetItem, Scan, Query, DeleteItem
- SNS: Publish

## Troubleshooting

**DynamoDB Connection Issues:**
```bash
aws dynamodb list-tables
aws sts get-caller-identity
```

**View Logs:**
```bash
eb logs
```

**Update Application:**
```bash
eb deploy
```

## Cost Information

- **Free Tier:** $0/month (first 12 months)
- **After Free Tier:** ~$14/month
  - EC2 t2.micro: $8/month
  - DynamoDB: $4/month
  - SNS: $2/month
