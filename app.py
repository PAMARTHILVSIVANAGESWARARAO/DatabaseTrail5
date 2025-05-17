from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # change this in production

MONGODB_URL = os.getenv("MONGODB_URL")
client = MongoClient(MONGODB_URL)
db = client.FirstProjectOnMongoDB
users_collection = db.users

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if not username or not password:
            return "Please provide both username and password."

        if users_collection.find_one({"username": username}):
            return "Username already exists, try another."

        users_collection.insert_one({"username": username, "password": password})
        return f"Registration successfully dear user {username} <br><a href='/signin'>Go to Sign In</a>"

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        user = users_collection.find_one({"username": username})
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid username or password. <br><a href='/signin'>Try again</a>"

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
