from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import database

app = Flask(__name__)
app.secret_key = "secret123"

# create tables
database.create_table()
database.create_weight_table()


# HOME
@app.route('/')
def home():
    return redirect('/register')


# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name,email,password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")


# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]

            return redirect('/dashboard')

        else:
            return "Invalid Login"

    return render_template("login.html")


# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect('/login')


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # get all weight records
    cursor.execute(
        "SELECT weight, target_weight FROM weight_tracker WHERE user_id=? ORDER BY id",
        (session['user_id'],)
    )

    rows = cursor.fetchall()

    conn.close()

    if rows:

        start_weight = float(rows[0][0])
        current_weight = float(rows[-1][0])
        target_weight = float(rows[0][1])

        remaining = round(target_weight - current_weight,2)

        # calculate progress
        if start_weight > target_weight:  # weight loss
            progress = ((start_weight - current_weight) / (start_weight - target_weight)) * 100
        else:  # weight gain
            progress = ((current_weight - start_weight) / (target_weight - start_weight)) * 100

        progress = max(0, min(progress, 100))
        progress = round(progress,1)

    else:
        current_weight = "-"
        target_weight = "-"
        remaining = "-"
        progress = 0

    return render_template(
        "dashboard.html",
        name=session['user_name'],
        current_weight=current_weight,
        target_weight=target_weight,
        remaining=remaining,
        progress=progress
    )

# BMI CALCULATOR
@app.route('/bmi', methods=['GET','POST'])
def bmi():

    if request.method == "POST":

        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        gender = request.form['gender']

        height_m = height / 100
        bmi_value = weight / (height_m * height_m)

        if bmi_value < 18.5:
            category = "Underweight"

        elif bmi_value < 24.9:
            category = "Normal"

        elif bmi_value < 29.9:
            category = "Overweight"

        else:
            category = "Obese"

        min_weight = 18.5 * (height_m * height_m)
        max_weight = 24.9 * (height_m * height_m)

        if weight < min_weight:
            change = round(min_weight - weight,2)
            suggestion = f"You should gain about {change} kg to reach a healthy weight."

        elif weight > max_weight:
            change = round(weight - max_weight,2)
            suggestion = f"You should lose about {change} kg to reach a healthy weight."

        else:
            suggestion = "Your weight is within the healthy range."

        return render_template(
            "bmi.html",
            bmi=round(bmi_value,2),
            category=category,
            min_weight=round(min_weight,2),
            max_weight=round(max_weight,2),
            suggestion=suggestion
        )

    return render_template("bmi.html")


# DIET PLAN GENERATOR
@app.route('/diet', methods=['GET','POST'])
def diet():

    if request.method == "POST":

        bmi_category = request.form.get('bmi_category')
        age = request.form.get('age')
        gender = request.form.get('gender')
        diet_type = request.form.get('diet_type')

        current_weight = request.form.get('current_weight')
        target_weight = request.form.get('target_weight')

        if not current_weight or not target_weight:
            return render_template("diet.html", error="Please enter current and target weight")

        current_weight = float(current_weight)
        target_weight = float(target_weight)

        if target_weight > current_weight:
            goal = "Weight Gain"
        elif target_weight < current_weight:
            goal = "Weight Loss"
        else:
            goal = "Maintain Weight"

        veg_plans = {

            "Weight Gain":{
                "Breakfast":"Milk, Banana smoothie, Peanut butter toast",
                "Snack1":"Dry fruits and nuts",
                "Lunch":"Rice, Dal, Paneer curry, Salad",
                "Snack2":"Fruit smoothie",
                "Dinner":"Roti, Mixed vegetable curry, Curd"
            },

            "Maintain Weight":{
                "Breakfast":"Oats with milk and fruits",
                "Snack1":"Apple and almonds",
                "Lunch":"2 Roti, Dal, Vegetable curry, Salad",
                "Snack2":"Green tea and roasted chana",
                "Dinner":"Brown rice, Paneer curry, Vegetables"
            },

            "Weight Loss":{
                "Breakfast":"Oats with chia seeds and fruits",
                "Snack1":"Green tea and fruit",
                "Lunch":"2 Roti, Mixed vegetable curry, Salad",
                "Snack2":"Buttermilk",
                "Dinner":"Vegetable soup and salad"
            }
        }

        nonveg_plans = {

            "Weight Gain":{
                "Breakfast":"Egg omelette, Milk, Whole wheat toast",
                "Snack1":"Nuts and banana",
                "Lunch":"Rice, Chicken curry, Vegetables",
                "Snack2":"Protein smoothie",
                "Dinner":"Grilled fish, Roti, Salad"
            },

            "Maintain Weight":{
                "Breakfast":"Boiled eggs, Oats",
                "Snack1":"Fruit and nuts",
                "Lunch":"Grilled chicken, Brown rice, Salad",
                "Snack2":"Green tea",
                "Dinner":"Fish, Vegetables"
            },

            "Weight Loss":{
                "Breakfast":"Boiled eggs and green tea",
                "Snack1":"Fruit",
                "Lunch":"Grilled chicken salad",
                "Snack2":"Buttermilk",
                "Dinner":"Fish soup and vegetables"
            }
        }

        if diet_type == "Vegetarian":
            plan = veg_plans[goal]
        else:
            plan = nonveg_plans[goal]

        return render_template("diet.html", goal=goal, plan=plan)

    return render_template("diet.html")


# WEIGHT TRACKER
import matplotlib.pyplot as plt
import os

@app.route('/tracker', methods=['GET','POST'])
def tracker():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        weight = request.form.get('weight')
        date = request.form.get('date')
        target_weight = request.form.get('target_weight')

        # check if target already exists
        cursor.execute(
            "SELECT target_weight FROM weight_tracker WHERE user_id=? LIMIT 1",
            (session['user_id'],)
        )

        target = cursor.fetchone()

        # reuse existing target
        if target:
            target_weight = target[0]

        cursor.execute(
            "INSERT INTO weight_tracker(user_id,date,weight,target_weight) VALUES(?,?,?,?)",
            (session['user_id'], date, weight, target_weight)
        )

        conn.commit()

    # fetch records
    cursor.execute(
        "SELECT date, weight, target_weight FROM weight_tracker WHERE user_id=? ORDER BY date",
        (session['user_id'],)
    )

    records = cursor.fetchall()
    conn.close()

    # determine if target exists
    target = None
    if records:
        target = records[0][2]

    # graph file path
    graph_path = os.path.join("static", "progress.png")

    # generate graph
    if records:

        dates = [row[0] for row in records]
        weights = [float(row[1]) for row in records]
        target_value = float(records[0][2])

        last_weight = weights[-1]

        # color logic
        if abs(last_weight - target_value) <= 1:
            color = "green"
        elif abs(last_weight - target_value) <= 3:
            color = "blue"
        else:
            color = "red"

        plt.figure(figsize=(6,4))

        plt.plot(dates, weights, marker='o', color=color, linewidth=3, label="Weight")

        plt.fill_between(dates, weights, color=color, alpha=0.2)

        plt.axhline(y=target_value, linestyle='--', color="black", label="Target")

        plt.xlabel("Date")
        plt.ylabel("Weight (kg)")
        plt.title("Weight Progress")

        plt.legend()

        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

    else:
        # delete old graph if no records exist
        if os.path.exists(graph_path):
            os.remove(graph_path)

    return render_template("tracker.html", records=records, target=target)
@app.route('/delete_tracker')
def delete_tracker():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM weight_tracker WHERE user_id=?",
        (session['user_id'],)
    )

    conn.commit()
    conn.close()

    return redirect('/tracker')

conv = {

"hi": "Hello! I am your health assistant. Ask me about BMI, diet, or weight progress.",

"hello": "Hello! I am your health assistant. Ask me about BMI, diet, or weight progress.",

"bmi": "BMI (Body Mass Index) helps determine whether your weight is healthy for your height.",

"diet": "You can generate a personalized diet plan in the Diet Plan Generator section of the app.",

"lose weight": "To lose weight: eat high-protein foods, reduce sugar, and exercise regularly.",

"gain weight": "To gain weight: eat calorie-rich foods like nuts, milk, bananas and do strength training.",

"exercise": "Try at least 30 minutes of exercise daily such as walking, running, or yoga.",

"tips": "Health Tip: Drink enough water, sleep 7-8 hours, and maintain a balanced diet."

}

@app.route('/chatbot', methods=['POST'])
def chatbot():

    data = request.json
    message = data.get("message").lower()

    user_name = session.get('user_name', "User")

    found = False

    for key in conv:

        if key in message:

            reply = conv[key]
            found = True
            break

    if not found:

        if "weight" in message or "progress" in message:

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT weight,target_weight FROM weight_tracker WHERE user_id=? ORDER BY id DESC LIMIT 1",
                (session['user_id'],)
            )

            record = cursor.fetchone()
            conn.close()

            if record:
                reply = f"Your current weight is {record[0]} kg and your target weight is {record[1]} kg."
            else:
                reply = "You haven't added weight records yet. Go to Weight Tracker."

        else:
            reply = "Sorry, I didn't understand. You can ask about BMI, diet, weight, or health tips."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)