from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def db_connection():
    conn = sqlite3.connect('setupdb.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Function to ensure the 'tickets' table exists
def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          departure TEXT NOT NULL,
                          destination TEXT NOT NULL,
                          day TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Call create_table function to ensure table exists
create_table()

# Create (C)
@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    # Validate that required fields are in the JSON payload
    if not data or not all(key in data for key in ['name', 'from', 'to', 'day']):
        return jsonify({"error": "Missing required fields"}), 400

    name = data['name']
    departure = data['from']
    destination = data['to']
    day = data['day']

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (name, departure, destination, day) VALUES (?, ?, ?, ?)", 
                   (name, departure, destination, day))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ticket created successfully"}), 201

# Read All (R - List)
@app.route('/tickets', methods=['GET'])
def get_tickets():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in tickets]), 200

# Read One (R)
@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    if ticket:
        return jsonify(dict(ticket)), 200
    return jsonify({"error": "Ticket not found"}), 404

# Update (U)
@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.get_json()
    # Validate that required fields are in the JSON payload
    if not data or not all(key in data for key in ['name', 'from', 'to', 'day']):
        return jsonify({"error": "Missing required fields"}), 400

    name = data['name']
    departure = data['from']
    destination = data['to']
    day = data['day']

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET name = ?, departure = ?, destination = ?, day = ? WHERE id = ?", 
                   (name, departure, destination, day, ticket_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ticket updated successfully"}), 200

# Delete (D)
@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ticket deleted successfully"}), 200

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
