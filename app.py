from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database file path
DATABASE = 'database.db'

def init_db():
    """Initialize the database with users table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            martial_status TEXT NOT NULL,
            gender TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Render the main form page"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    if request.method == 'POST':
        # Get form data
        full_name = request.form['fullname']
        email = request.form['email']
        martial_status = request.form['martial-status']
        gender = request.form['gender']
        dob = request.form['dob']
        
        # Validate required fields
        if not all([full_name, email, martial_status, gender, dob]):
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))
        
        try:
            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (full_name, email, martial_status, gender, date_of_birth)
                VALUES (?, ?, ?, ?, ?)
            ''', (full_name, email, martial_status, gender, dob))
            
            conn.commit()
            conn.close()
            
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
            
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/users')
def list_users():
    """Display all registered users"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    import sys
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, using default 5000")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=port)

