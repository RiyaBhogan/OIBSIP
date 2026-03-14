SecurePass – Password Security Dashboard

SecurePass is a web-based password security application built using Flask. The system helps users generate strong passwords, analyze password strength using machine learning, check whether a password has appeared in known data breaches, and securely store credentials using encryption.

The application integrates password generation, machine learning based strength prediction, breach detection using an external API, and a secure password manager with user authentication.

Features
User Authentication

User registration system

Secure login using password hashing

Session-based authentication

Logout functionality

Password Generator

Generate strong passwords based on user-defined criteria

Custom number of uppercase letters, lowercase letters, numbers, and symbols

Randomized password generation

Password Strength Prediction (Machine Learning)

Machine learning model evaluates password strength

Calculates password entropy

Predicts approximate password cracking time

Password Breach Detection

Checks if a password has appeared in known data breaches

Uses the HaveIBeenPwned API with SHA-1 hashing and k-anonymity

Secure Password Manager

Save login credentials for websites

Passwords encrypted using Fernet symmetric encryption

Retrieve and decrypt stored passwords

Delete saved credentials

Technologies Used
Backend

Python

Flask

Machine Learning

Scikit-learn

Joblib

Database

SQLite

Security

Werkzeug Password Hashing

Cryptography (Fernet Encryption)

SHA-1 Hashing for breach checking

API

HaveIBeenPwned Password API

Other Libraries

Requests

Random

String

Hashlib

Project Structure
SecurePass
│
├── app.py
├── passwords.db
├── secret.key
│
├── models
│   ├── strength_model.pkl
│   └── time_model.pkl
│
├── utils.py
│
├── templates
│   └── index.html
│
└── static
    ├── css
    ├── js
    └── images
Installation

Clone the repository

git clone https://github.com/RiyaBhogan/OIBSIP.git

Navigate to the project directory

cd OIBSIP/OIBSIP_Python_Task3

Install required dependencies

pip install flask cryptography requests joblib scikit-learn werkzeug

Run the application

python app.py

Open the application in your browser

http://127.0.0.1:5000
Database

The application uses SQLite database passwords.db with the following tables:

Users Table

id

username

password (hashed)

Passwords Table

id

user_id

website

username

password (encrypted)

Security Implementation

The project implements several security mechanisms:

Password hashing using Werkzeug

Encryption of stored passwords using Fernet symmetric encryption

Secure session management

SHA-1 hashing for privacy-preserving breach detection

K-anonymity approach when querying the breach database

Machine Learning Models

Two machine learning models are used in the application:

Strength Prediction Model
Predicts the strength category of a password based on features such as entropy and length.

Crack Time Prediction Model
Estimates the approximate time required to crack the password.

These models are loaded using Joblib during application startup.

Future Improvements

Password pattern detection

Two-factor authentication

Password sharing with encryption

Browser extension integration

Password strength visualization charts
