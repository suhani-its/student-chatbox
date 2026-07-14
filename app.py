from flask import Flask, render_template, request, jsonify, redirect, session
import json
import random
from google import genai
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ========== 1. API KEY SETUP ==========

client = genai.Client(api_key="AQ.Ab8RN6IQeC36S1pDO-5CiPEfg7oVg-9pdInWW2qf69MAzMY0CAm")
# ========== 2. DATABASE SETUP ==========
conn = sqlite3.connect('college.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students (rollno TEXT PRIMARY KEY, name TEXT, attendance REAL, fees_status TEXT)''')
c.execute("INSERT OR IGNORE INTO students VALUES ('101', 'Riya', 85.5, 'Paid')")
c.execute("INSERT OR IGNORE INTO students VALUES ('102', 'Aman', 72.0, 'Pending')")
conn.commit()

# ========== 3. intents.json LOAD ==========
with open('intents.json', encoding='utf-8') as f:
    data = json.load(f)

# ========== 4. MAIN LOGIC FUNCTION ==========
def get_response(user_message):
    user_message = user_message.lower()
    # 1. Pehle intents.json check
    for intent in data['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_message:
                return random.choice(intent['responses'])

    # 2. Attendance check
    if "attendance" in user_message:
        c.execute("SELECT name, attendance FROM students WHERE rollno='101'")
        result = c.fetchone()
        if result:
            return f"{result[0]}, tumhari attendance {result[1]}% hai"

    # 3. Fees check
    if "fees" in user_message:
        c.execute("SELECT name, fees_status FROM students WHERE rollno='101'")
        result = c.fetchone()
        if result:
            return f"{result[0]}, tumhari fees status: {result[1]}"

    # 4. AI se p = pucho - naya tarika
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"You are a college student support bot. Reply in simple Hindi. Question: {user_message}"
        )
        return response.text
    except:
        return "Sorry, AI se connect nahi ho pa raha."

# ========== 5. FLASK ROUTES ==========
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    session['student'] = request.form['name']
    return redirect('/chat')

@app.route('/chat')
def chat():
    if 'student' not in session:
        return redirect('/')
    return render_template('chat.html')

@app.route('/get', methods=['POST'])
def get():
    user_message = request.form['message']
    bot_reply = get_response(user_message)
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)