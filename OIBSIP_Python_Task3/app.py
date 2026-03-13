from flask import Flask, render_template, request, jsonify, session, redirect
import random
import string
import hashlib
import requests
from cryptography.fernet import Fernet
import sqlite3
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
from utils import extract_features, convert_time

app = Flask(__name__)
app.secret_key = "supersecretkey"

strength_model = joblib.load("models/strength_model.pkl")
time_model = joblib.load("models/time_model.pkl")

# ---------------- ENCRYPTION KEY ----------------

try:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
except:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

cipher = Fernet(key)

# ---------------- DATABASE ----------------

def init_db():

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        website TEXT,
        username TEXT,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------

@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    password = generate_password_hash(request.form["password"])

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    try:

        cur.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username,password)
        )

        conn.commit()

        return jsonify({"message":"User registered successfully"})

    except sqlite3.IntegrityError:

        return jsonify({"message":"Username already exists"})

    finally:
        conn.close()

# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    cur.execute(
    "SELECT id,password FROM users WHERE username=?",
    (username,)
    )

    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user[1], password):

        session["user_id"] = user[0]

        return jsonify({"success": True})

    return jsonify({"success": False})

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect("/")

# ---------------- PASSWORD GENERATOR ----------------

def generate_password(upperCount, lowerCount, numberCount, symbolCount):

    password_chars = []

    for i in range(upperCount):
        password_chars.append(random.choice(string.ascii_uppercase))

    for i in range(lowerCount):
        password_chars.append(random.choice(string.ascii_lowercase))

    for i in range(numberCount):
        password_chars.append(random.choice(string.digits))

    for i in range(symbolCount):
        password_chars.append(random.choice("!@#$%^&*()"))

    random.shuffle(password_chars)

    return ''.join(password_chars)

@app.route("/generate", methods=["POST"])
def generate():

    upperCount = int(request.form.get("upperCount"))
    lowerCount = int(request.form.get("lowerCount"))
    numberCount = int(request.form.get("numberCount"))
    symbolCount = int(request.form.get("symbolCount"))

    password = generate_password(
        upperCount,
        lowerCount,
        numberCount,
        symbolCount
    )

    return jsonify({"password": password})

# ---------------- ML PASSWORD STRENGTH ----------------

@app.route("/predict", methods=["POST"])
def predict():

    password = request.form.get("password")

    strength, length, entropy = extract_features(password)

    features = [[strength,length,entropy]]

    class_strength = strength_model.predict(features)[0]
    crack_time_sec = time_model.predict(features)[0]

    crack_time = convert_time(crack_time_sec)

    return jsonify({
        "class_strength": class_strength,
        "entropy": round(entropy,2),
        "crack_time": crack_time
    })

# ---------------- BREACH CHECK ----------------

def check_password_breach(password):

    sha1password = hashlib.sha1(password.encode()).hexdigest().upper()

    prefix = sha1password[:5]
    suffix = sha1password[5:]

    url = "https://api.pwnedpasswords.com/range/" + prefix

    res = requests.get(url)

    hashes = (line.split(":") for line in res.text.splitlines())

    for h, count in hashes:
        if h == suffix:
            return True

    return False

@app.route("/check_breach", methods=["POST"])
def check_breach():

    password = request.form.get("password")

    breached = check_password_breach(password)

    return jsonify({"breached": breached})

# ---------------- PASSWORD MANAGER ----------------

@app.route("/save_password", methods=["POST"])
def save_password():

    if "user_id" not in session:
        return jsonify({"error":"login required"}),401

    user_id = session["user_id"]

    website = request.form.get("website")
    username = request.form.get("username")
    password = request.form.get("password")

    encrypted_password = cipher.encrypt(password.encode())

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    cur.execute(
    "INSERT INTO passwords(user_id,website,username,password) VALUES(?,?,?,?)",
    (user_id,website,username,encrypted_password)
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"saved"})

# ---------------- GET SAVED PASSWORDS ----------------

@app.route("/get_passwords")
def get_passwords():

    if "user_id" not in session:
        return jsonify({"error":"login required"}),401

    user_id = session["user_id"]

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    cur.execute(
    "SELECT website,username,password FROM passwords WHERE user_id=?",
    (user_id,)
    )

    rows = cur.fetchall()

    result = []

    for row in rows:

        decrypted = cipher.decrypt(row[2]).decode()

        result.append({
            "website": row[0],
            "username": row[1],
            "password": decrypted
        })

    conn.close()

    return jsonify(result)

# ---------------- DELETE PASSWORD ----------------

@app.route("/delete_password", methods=["POST"])
def delete_password():

    if "user_id" not in session:
        return jsonify({"error":"login required"}),401

    user_id = session["user_id"]
    website = request.form.get("website")
    username = request.form.get("username")

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    cur.execute(
    "DELETE FROM passwords WHERE website=? AND username=? AND user_id=?",
    (website, username, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"deleted"})

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)