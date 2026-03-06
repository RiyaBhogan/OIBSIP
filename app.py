from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

# NEW IMPORTS FOR REMINDER SYSTEM
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from plyer import notification
from gtts import gTTS
from playsound import playsound
import os

app = Flask(__name__)
app.secret_key = "office_secret"

SENDER_EMAIL = "riya1970463@gmail.com"
APP_PASSWORD = "tcrhsbphogvizyli"


# ================= REMINDER CHECK FUNCTION =================
def check_reminders():

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    now_date = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")

    cursor.execute(
        "SELECT id, title FROM reminders WHERE date=? AND time=?",
        (now_date, now_time)
    )

    reminders = cursor.fetchall()

    for r in reminders:

        reminder_id = r[0]
        title = r[1]

        msg = f"Reminder: {title}"
        print(msg)

        # Desktop Notification
        notification.notify(
            title="Office Reminder",
            message=msg,
            timeout=10
        )

        # Voice Alert
        audio = gTTS(text=msg)
        filename = "reminder.mp3"

        audio.save(filename)
        playsound(filename)
        os.remove(filename)

        # Delete reminder after alert
        cursor.execute(
            "DELETE FROM reminders WHERE id=?",
            (reminder_id,)
        )

    conn.commit()
    conn.close()

# ================= START SCHEDULER =================
scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, 'interval', minutes=1)
scheduler.start()

#==================delete reminder==================
@app.route("/delete_reminder/<int:id>")
def delete_reminder(id):

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reminders WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Reminder deleted successfully")

    return redirect(url_for("reminders"))


# ================= LOGIN =================
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("office.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (email,password)
        )

        result = cursor.fetchone()
        conn.close()

        if result:

            session["email"] = email
            session["role"] = result[0]

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid Login Credentials")
            return redirect(url_for("login"))

    return render_template("login.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    # Emails sent today
    cursor.execute("""
    SELECT COUNT(*) FROM email_logs
    WHERE DATE(timestamp) = DATE('now')
    """)
    email_count = cursor.fetchone()[0]

    # Upcoming meetings
    cursor.execute("""
    SELECT COUNT(*) FROM meetings
    WHERE date >= DATE('now')
    """)
    meeting_count = cursor.fetchone()[0]

    # Pending tasks for logged-in user
    cursor.execute("""
    SELECT COUNT(*) FROM tasks
    WHERE user_email=? AND status='Pending'
    """, (session["email"],))

    pending_tasks = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        role=session["role"],
        user=session["email"],
        email_count=email_count,
        meeting_count=meeting_count,
        pending_tasks=pending_tasks
    )
# ================= SEND EMAIL =================
@app.route("/email", methods=["GET","POST"])
def email():

    if "email" not in session:
        return redirect(url_for("login"))

    if session["role"] not in ["hr","manager"]:
        return "Access Denied"

    if request.method == "POST":

        group = request.form["group"]
        subject = request.form["subject"]
        body = request.form["body"]

        if not subject or not body:
            flash("Subject and message cannot be empty")
            return redirect(url_for("email"))

        emails = []

        with open("contacts.csv") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["group"] == group:
                    emails.append(row["email"])

        with SMTP("smtp.gmail.com",587) as server:

            server.starttls()
            server.login(SENDER_EMAIL,APP_PASSWORD)

            for email in emails:

                msg = MIMEMultipart()

                msg["From"] = SENDER_EMAIL
                msg["To"] = email
                msg["Subject"] = subject

                msg.attach(MIMEText(body,"plain"))

                server.sendmail(
                    SENDER_EMAIL,
                    email,
                    msg.as_string()
                )

        conn = sqlite3.connect("office.db")
        cursor = conn.cursor()

        cursor.execute(
        """
        INSERT INTO email_logs(sender, group_name, subject)
        VALUES (?, ?, ?)
        """,
        (session["email"], group, subject)
        )

        conn.commit()
        conn.close()

        flash(f"Emails sent successfully to {group}")

        return redirect(url_for("email"))

    return render_template("email.html")


# ================= EMAIL HISTORY =================
@app.route("/email_history")
def email_history():

    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT sender, group_name, subject, timestamp
    FROM email_logs
    ORDER BY timestamp DESC
    """)

    logs = cursor.fetchall()
    conn.close()

    return render_template("email_history.html", logs=logs)


# ================= MEETINGS =================
@app.route("/meetings", methods=["GET","POST"])
def meetings():

    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    if request.method == "POST":

        if session["role"] not in ["hr","manager"]:
            return "Access Denied"

        title = request.form["title"]
        date = request.form["date"]
        time = request.form["time"]

        cursor.execute(
        "INSERT INTO meetings(title,date,time,created_by) VALUES (?,?,?,?)",
        (title,date,time,session["email"])
        )

        conn.commit()

        flash("Meeting scheduled successfully")

        return redirect(url_for("meetings"))

    cursor.execute(
        "SELECT * FROM meetings ORDER BY date,time"
    )

    meetings = cursor.fetchall()
    conn.close()

    return render_template(
        "meetings.html",
        meetings=meetings,
        role=session["role"]
    )

#=====================Delete meeting===============
@app.route("/delete_meeting/<int:id>")
def delete_meeting(id):

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM meetings WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Meeting deleted successfully")

    return redirect(url_for("meetings"))

#===================Edit meeting==================
@app.route("/edit_meeting/<int:id>", methods=["GET","POST"])
def edit_meeting(id):

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        date = request.form["date"]
        time = request.form["time"]

        cursor.execute(
        "UPDATE meetings SET title=?, date=?, time=? WHERE id=?",
        (title,date,time,id)
        )

        conn.commit()
        conn.close()

        flash("Meeting updated successfully")

        return redirect(url_for("meetings"))

    cursor.execute("SELECT * FROM meetings WHERE id=?", (id,))
    meeting = cursor.fetchone()

    conn.close()

    return render_template("edit_meeting.html", meeting=meeting)
# ================= TASKS =================
@app.route("/tasks", methods=["GET","POST"])
def tasks():

    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        date = request.form["date"]
        time = request.form.get("time")

        cursor.execute(
        "INSERT INTO tasks(title,date,time,status,user_email) VALUES (?,?,?,?,?)",
        (title,date,time,"Pending",session["email"])
        )

        conn.commit()
        flash("Task added successfully")

        return redirect(url_for("tasks"))

    cursor.execute(
    "SELECT * FROM tasks WHERE user_email=? ORDER BY date,time",
    (session["email"],)
    )

    tasks = cursor.fetchall()
    conn.close()

    return render_template("tasks.html", tasks=tasks)
#========================Complete Task=====================
@app.route("/complete_task/<int:id>")
def complete_task(id):

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Task marked as completed")

    return redirect(url_for("tasks"))
#======================Delete Task===========================
@app.route("/delete_task/<int:id>")
def delete_task(id):

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Task deleted successfully")

    return redirect(url_for("tasks"))

# ================= REMINDERS =================
@app.route("/reminders", methods=["GET","POST"])
def reminders():

    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("office.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        date = request.form["date"]
        time = request.form["time"]

        cursor.execute(
        "INSERT INTO reminders(title,date,time,user_email) VALUES (?,?,?,?)",
        (title,date,time,session["email"])
        )

        conn.commit()
        flash("Reminder added successfully")

        return redirect(url_for("reminders"))

    cursor.execute(
    "SELECT * FROM reminders WHERE user_email=? ORDER BY date,time",
    (session["email"],)
    )

    reminders = cursor.fetchall()
    conn.close()

    return render_template(
        "reminders.html",
        reminders=reminders
    )


# ================= LOGOUT =================
@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)