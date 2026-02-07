<div align="center">

# 🏥 MedTrack - Healthcare Management System

### *Modern Healthcare Appointment & Management Platform*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![AWS](https://img.shields.io/badge/AWS-Ready-orange.svg)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A comprehensive healthcare management web application with AWS cloud integration**

[Features](#-features) • [Quick Start](#-quick-start) • [AWS Deployment](#-aws-deployment) • [Documentation](#-documentation)

---

**Author:** Nadeem | **Email:** nadeem.221751.cs@mhssce.ac.in | **Institution:** MHSSCE

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 👨‍⚕️ For Healthcare Providers
- 🏥 Professional dashboard
- 📊 Patient management
- 📅 Appointment scheduling
- 📋 Medical records access
- 🔔 Real-time notifications

</td>
<td width="50%">

### 👤 For Patients
- 📱 Easy appointment booking
- 🗓️ View appointment history
- 👨‍⚕️ Doctor selection
- 📝 Medical history tracking
- ✉️ Email notifications

</td>
</tr>
</table>

### 🚀 Technical Features
- ✅ **Dual Mode**: Local development (in-memory) & AWS production (DynamoDB)
- ✅ **Cloud-Ready**: Full AWS integration with DynamoDB and SNS
- ✅ **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- ✅ **Secure**: Session-based authentication with Flask
- ✅ **Scalable**: Ready for production deployment
- ✅ **CI/CD**: GitHub Actions workflow included

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.8 or higher
- pip package manager
- AWS account (for cloud deployment)

### 💻 Local Development

```bash
# 1. Clone the repository
git clone https://github.com/nadeem860/medtrack-healthcare-aws.git
cd medtrack-healthcare-aws

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

🌐 **Visit:** http://localhost:5000

🔐 **Demo Credentials:**
- **Patient:** `patient@demo.com` / `password123`
- **Doctor:** `doctor@demo.com` / `password123`

## ☁️ AWS Deployment

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
chmod +x quick_start_aws.sh
./quick_start_aws.sh
```

### Option 2: Manual Setup

**Step 1: Create DynamoDB Tables**
```bash
python create_dynamodb_tables.py
```

**Step 2: Configure Environment**
```bash
export USE_AWS=true
export AWS_REGION=us-east-1
export SECRET_KEY='your-secure-random-key'
export SNS_TOPIC_ARN='your-sns-topic-arn'  # Optional
```

**Step 3: Deploy to Elastic Beanstalk**
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init -p python-3.8 medtrack-app --region us-east-1
eb create medtrack-env
eb open
```

### Option 3: EC2 Manual Deployment

```bash
# On EC2 instance
git clone https://github.com/nadeem860/medtrack-healthcare-aws.git
cd medtrack-healthcare-aws
pip3 install -r requirements.txt

# Set environment variables
export USE_AWS=true
export AWS_REGION=us-east-1
export SECRET_KEY='your-key'

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:80 aws_app:app
```

📖 **Detailed Guide:** See [AWS_SETUP.md](AWS_SETUP.md) for complete instructions

## 📁 Project Structure

```
medtrack-healthcare-aws/
│
├── 🐍 Application Files
│   ├── app.py                      # Local development (in-memory storage)
│   ├── aws_app.py                  # Production (DynamoDB + SNS)
│   └── create_dynamodb_tables.py   # DynamoDB setup script
│
├── ⚙️ Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── Procfile                    # Elastic Beanstalk config
│   ├── .env.example                # Environment variables template
│   └── .gitignore                  # Git exclusions
│
├── 🌐 Frontend
│   ├── templates/                  # HTML templates (10 files)
│   │   ├── base.html              # Base template
│   │   ├── index.html             # Landing page
│   │   ├── login.html             # Login page
│   │   ├── signup.html            # Registration
│   │   ├── patient_dashboard.html # Patient dashboard
│   │   ├── doctor_dashboard.html  # Doctor dashboard
│   │   ├── booking.html           # Appointment booking
│   │   └── ...
│   └── static/                     # Static assets
│       ├── css/style.css          # Custom styles
│       ├── js/main.js             # JavaScript
│       └── images/                # Images
│
├── ☁️ AWS Configuration
│   ├── .ebextensions/             # Elastic Beanstalk settings
│   └── .github/workflows/         # GitHub Actions CI/CD
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── AWS_SETUP.md                # AWS deployment guide
    └── LICENSE                     # MIT License
```

## 🔧 Technology Stack

<table>
<tr>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /><br>
<b>Python 3.8+</b>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /><br>
<b>Flask 2.3.3</b>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" /><br>
<b>Bootstrap 5</b>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" /><br>
<b>AWS Cloud</b>
</td>
</tr>
</table>

### Backend
- **Flask** - Web framework
- **boto3** - AWS SDK for Python
- **Gunicorn** - WSGI HTTP Server

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive framework
- **JavaScript** - Client-side functionality
- **Font Awesome** - Icons

### AWS Services
- **DynamoDB** - NoSQL database for scalable storage
- **SNS** - Simple Notification Service for alerts
- **Elastic Beanstalk** - Platform as a Service
- **EC2** - Virtual servers
- **IAM** - Identity and Access Management

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `USE_AWS` | Yes | `false` | Enable AWS services (`true`/`false`) |
| `AWS_REGION` | Yes | `us-east-1` | AWS region for services |
| `SECRET_KEY` | Yes | - | Flask session secret key |
| `SNS_TOPIC_ARN` | No | - | SNS topic ARN for notifications |
| `USERS_TABLE` | No | `MedTrack_Users` | DynamoDB users table name |
| `APPOINTMENTS_TABLE` | No | `MedTrack_Appointments` | DynamoDB appointments table |
| `FLASK_ENV` | No | `development` | Flask environment mode |

### Example Configuration

```bash
# .env file
USE_AWS=true
AWS_REGION=us-east-1
SECRET_KEY=your-secure-random-key-here
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:MedTrack-Notifications
FLASK_ENV=production
```

## 💰 Cost Estimation

### AWS Free Tier (First 12 Months)
| Service | Free Tier | Cost |
|---------|-----------|------|
| EC2 (t2.micro) | 750 hours/month | **$0** |
| DynamoDB | 25 GB storage + 25 RCU/WCU | **$0** |
| SNS | 1,000 email notifications | **$0** |
| **Total** | | **$0/month** |

### After Free Tier (Low Traffic)
| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| EC2 (t2.micro) | 24/7 | ~$8 |
| DynamoDB (3 tables) | Low traffic | ~$4 |
| SNS | Moderate usage | ~$2 |
| **Total** | | **~$14/month** |

💡 **Tip:** Use AWS Cost Calculator for accurate estimates based on your usage.

## 📚 Documentation

- **[README.md](README.md)** - This file (Quick start guide)
- **[AWS_SETUP.md](AWS_SETUP.md)** - Complete AWS deployment guide
- **[LICENSE](LICENSE)** - MIT License details

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open a Pull Request

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Nadeem**
- 📧 Email: nadeem.221751.cs@mhssce.ac.in
- 🏫 Institution: MHSSCE
- 💼 GitHub: [@nadeem860](https://github.com/nadeem860)

## 🙏 Acknowledgments

- Flask framework and community
- AWS documentation and services
- Bootstrap for responsive design
- Font Awesome for icons
- All contributors and supporters

## 📞 Support

For issues, questions, or contributions:

1. 📖 Check the [documentation](AWS_SETUP.md)
2. 🐛 Open an [issue](https://github.com/nadeem860/medtrack-healthcare-aws/issues)
3. 📧 Contact: nadeem.221751.cs@mhssce.ac.in

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Built with ❤️ for better healthcare management**

[⬆ Back to Top](#-medtrack---healthcare-management-system)

</div>
