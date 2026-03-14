\# Office Management System



The Office Management System is a Flask-based web application designed to manage office activities such as meetings, tasks, reminders, and email communication. It provides role-based access for employees, HR, and managers to organize daily work efficiently.



\## Features



User Authentication

\- Secure login system

\- Role-based access control (Employee, HR, Manager)



Bulk Email Sender

\- Send emails to specific groups using a CSV contact list

\- Email history logging

\- Gmail SMTP integration for sending emails



Meeting Scheduler

\- Schedule meetings with date and time

\- Edit existing meetings

\- Delete meetings

\- View upcoming meetings



Task Management

\- Add tasks with date and optional time

\- Mark tasks as completed

\- Delete tasks

\- View tasks assigned to the logged-in user



Reminder System

\- Create reminders for important events

\- Desktop notifications for reminders

\- Voice alerts using text-to-speech

\- Automatic reminder checking every minute



Dashboard

\- Displays number of emails sent today

\- Shows upcoming meetings

\- Displays pending tasks for the logged-in user



\## Technologies Used



Backend

\- Python

\- Flask



Database

\- SQLite



Libraries

\- APScheduler

\- Plyer (Desktop notifications)

\- gTTS (Google Text-to-Speech)

\- Playsound

\- smtplib (SMTP for email sending)



Frontend

\- HTML

\- CSS







