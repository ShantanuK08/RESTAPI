from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def db_connection():
    conn = sqlite3.connect('setupdb.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Function to ensure the 'items' table exists
def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          description TEXT)''')
    conn.commit()
    conn.close()

# Call create_table function to ensure table exists
create_table()

# Create (C)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item created successfully"}), 201

# Read (R)
@app.route('/items', methods=['GET'])
def get_items():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items]), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item:
        return jsonify(dict(item)), 200
    return jsonify({"error": "Item not found"}), 404

# Update (U)
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, description = ? WHERE id = ?", (name, description, item_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item updated successfully"}), 200

# Delete (D)
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item deleted successfully"}), 200

# List (L) is essentially the same as Read (GET /items)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)







    