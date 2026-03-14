Office Management System

The Office Management System is a web-based application developed using Flask and SQLite to help organizations manage internal office activities efficiently. The system provides functionalities such as meeting scheduling, task management, email communication, reminders, and dashboard analytics.

The application supports role-based access for employees, HR, and managers, allowing better coordination and organization of daily office tasks.

Features
User Authentication

Login system for office users

Session-based authentication

Role-based access control (Employee, HR, Manager)

Secure logout functionality

Dashboard

The dashboard provides a quick overview of office activities:

Total emails sent today

Number of upcoming meetings

Pending tasks for the logged-in user

Email Management

Send bulk emails to employee groups

Uses Gmail SMTP for sending emails

Reads recipient information from a CSV file

Stores email history in the database

Email History

Displays previously sent emails

Shows sender, group name, subject, and timestamp

Meeting Scheduler

Schedule new meetings with title, date, and time

Edit existing meetings

Delete meetings

View upcoming meetings

Task Management

Create tasks for users

Set task date and optional time

Mark tasks as completed

Delete tasks

View tasks assigned to the logged-in user

Reminder System

The system includes an automated reminder feature that checks scheduled reminders every minute.

When a reminder is triggered:

A desktop notification is displayed

A voice alert is played using text-to-speech

The reminder is automatically removed from the database

Technologies Used
Backend

Python

Flask

Database

SQLite

Email Service

SMTP (Gmail)

Scheduler

APScheduler

Notification System

Plyer (Desktop Notifications)

gTTS (Google Text-to-Speech)

Playsound

Frontend

HTML

CSS

Jinja2 Templates

Other Libraries

CSV

Datetime

OS

Project Structure
Office-Management-System
│
├── app.py
├── office.db
├── contacts.csv
│
├── templates
│   ├── login.html
│   ├── dashboard.html
│   ├── email.html
│   ├── email_history.html
│   ├── meetings.html
│   ├── edit_meeting.html
│   ├── tasks.html
│   └── reminders.html
│
└── static
    ├── css
    ├── js
    └── images
Installation
Clone the repository
git clone https://github.com/yourusername/office-management-system.git
Navigate to the project directory
cd office-management-system
Install required dependencies
pip install flask apscheduler plyer gtts playsound
Run the application
python app.py
Open the application in your browser
http://127.0.0.1:5000
Database

The application uses an SQLite database named office.db.

Users Table

Stores login credentials and roles:

id

username

password

role

Meetings Table

Stores meeting details:

id

title

date

time

created_by

Tasks Table

Stores tasks assigned to users:

id

title

date

time

status

user_email

Reminders Table

Stores reminder information:

id

title

date

time

user_email

Email Logs Table

Stores email communication history:

id

sender

group_name

subject

timestamp

Reminder System

The reminder system runs in the background using APScheduler and checks every minute for scheduled reminders.

When a reminder time matches the current system time:

A desktop notification is displayed

A voice reminder is generated using text-to-speech

The reminder is automatically deleted after execution

Email Configuration

The system uses Gmail SMTP to send emails.

Update the following values in app.py:

SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"

Use a Gmail App Password instead of your regular Gmail password.

Future Improvements

Password hashing for improved security

File attachments in emails

Calendar view for meetings

Mobile responsive interface

Role-based task assignment

Real-time notifications
