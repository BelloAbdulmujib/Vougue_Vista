import sqlite3
from flask import Flask, Blueprint
from extensions import db
from app.models import Admin

# Initialize the Flask app
app = Flask(__name__)
admin_data_bp = Blueprint('admin_data', __name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('instance/VogueVista.sqlite3') 
    conn.row_factory = sqlite3.Row  # Optional: allows access to columns by name
    return conn

# Function to insert data into the SQLite database
def insert_data():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL statement to insert data
    cursor.execute('''
        INSERT INTO admin (username, email, password)
        VALUES (?, ?, ?)
    ''', ('admin001', 'admin001@gmail.com', 'scrypt:32768:8:1$O57OrzwHbSgcrZT8$d372b061221f4d2cad46867d5e74c8c5c8cfb8e9aaef939e5cb76dae6b7f664f396493721ce4b19ba2b57892a5b2d49ce62430ae2a3f67f098a0132cd4415c13'))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return 'Data inserted successfully!'

# Define a route to trigger the data insertion
@admin_data_bp.route('/insert')
def insert():
    return insert_data()  # Call the insert_data function