from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route (GET)
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission (POST)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    # Save data to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

    return redirect('/')

# API route to get user data (AJAX request)
@app.route('/users', methods=['GET'])
def users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    # Return the data as JSON
    return jsonify(users)

if __name__ == '__main__':
    init_db()  # Initialize database when the app starts
    app.run(debug=True)