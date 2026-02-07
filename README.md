# MedTrack - Healthcare Management System

Flask-based healthcare management system with AWS DynamoDB and SNS integration.

**Author:** Nadeem (nadeem.221751.cs@mhssce.ac.in)

## Features

- Patient & Doctor registration and authentication
- Appointment booking system
- Patient and Doctor dashboards
- AWS DynamoDB for data persistence
- AWS SNS for notifications
- Responsive design with Bootstrap

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000  
Demo: patient@demo.com / password123

### AWS Deployment

**1. Create DynamoDB Tables:**
```bash
python create_dynamodb_tables.py
```

**2. Set Environment Variables:**
```bash
export USE_AWS=true
export AWS_REGION=us-east-1
export SECRET_KEY='your-secure-key'
```

**3. Deploy to Elastic Beanstalk:**
```bash
pip install awsebcli
eb init -p python-3.8 medtrack-app --region us-east-1
eb create medtrack-env
eb open
```

## Project Structure

```
medtrack/
├── app.py                      # Local development (in-memory)
├── aws_app.py                  # Production (DynamoDB + SNS)
├── create_dynamodb_tables.py   # DynamoDB setup script
├── requirements.txt            # Python dependencies
├── Procfile                    # EB configuration
├── templates/                  # HTML templates
├── static/                     # CSS, JS, images
└── .ebextensions/              # EB settings
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `USE_AWS` | Yes | Set to `true` for AWS mode |
| `AWS_REGION` | Yes | AWS region (e.g., us-east-1) |
| `SECRET_KEY` | Yes | Flask session secret |
| `SNS_TOPIC_ARN` | No | SNS topic for notifications |

## AWS Services Used

- **DynamoDB**: User and appointment data storage
- **SNS**: Email/SMS notifications
- **Elastic Beanstalk**: Application hosting
- **EC2**: Virtual servers

## Cost Estimate

**Free Tier (12 months):** $0/month  
**After Free Tier:** ~$14/month (low traffic)

## License

MIT License - See LICENSE file
