Health and Fitness Tracker Web Application

This project is a web-based Health and Fitness Tracker developed using Flask and SQLite. The application helps users monitor their health by calculating BMI, generating diet plans, tracking weight progress, and providing health-related chatbot assistance.

The system includes user authentication, weight tracking with graphical progress visualization, personalized diet suggestions, and a BMI calculator to help users maintain a healthy lifestyle.

Features
User Authentication

User registration system

Secure login using sessions

Logout functionality

User-specific data storage

Dashboard

Displays the user's current weight

Shows target weight

Calculates remaining weight to reach the goal

Displays progress percentage toward the goal

BMI Calculator

Calculates Body Mass Index (BMI) using height and weight

Categorizes BMI into:

Underweight

Normal

Overweight

Obese

Provides weight suggestions to reach a healthy range

Diet Plan Generator

Generates personalized diet plans based on:

Weight goal (Loss, Gain, Maintain)

Diet type (Vegetarian / Non-Vegetarian)

Includes structured daily meal plans such as:

Breakfast

Snacks

Lunch

Dinner

Weight Tracker

Allows users to record daily weight

Stores weight history in a database

Visualizes weight progress using a graph

Displays a target weight reference line

Color-coded progress based on proximity to the target weight

Health Chatbot

The chatbot provides responses related to:

BMI

Diet advice

Weight gain and loss tips

Exercise suggestions

General health tips

It can also retrieve the user's latest weight progress from the database.

Technologies Used
Backend

Python

Flask

Database

SQLite

Data Visualization

Matplotlib

Frontend

HTML

CSS

Jinja2 Templates

Other Libraries

SQLite3

OS

JSON

Project Structure
Health-Fitness-App
│
├── app.py
├── database.py
├── database.db
│
├── templates
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── bmi.html
│   ├── diet.html
│   ├── tracker.html
│
└── static
    ├── progress.png
    ├── css
    └── js
Installation
Clone the repository
git clone https://github.com/yourusername/health-fitness-app.git
Navigate to the project directory
cd health-fitness-app
Install required dependencies
pip install flask matplotlib
Run the application
python app.py
Open the application in your browser
http://127.0.0.1:5000
Database

The application uses SQLite database (database.db).

Users Table

Stores registered user information:

id

name

email

password

Weight Tracker Table

Stores user weight records:

id

user_id

date

weight

target_weight

Weight Progress Visualization

The system generates a graph showing the user’s weight progress over time.

The graph includes:

Weight trend line

Target weight reference line

Color-coded progress indicator

Date-based tracking

The graph is saved in the static folder and displayed in the tracker section.

Chatbot Functionality

The chatbot provides simple health guidance using predefined responses.

It can answer questions about:

BMI

Diet recommendations

Weight loss tips

Weight gain advice

Exercise suggestions

Health tips

It can also retrieve the user's latest weight and target weight from the database.

Future Improvements

Password hashing for better security

AI-based diet recommendation system

Advanced chatbot using NLP

Mobile responsive UI improvements

Weekly health analytics dashboard

Integration with fitness APIs
