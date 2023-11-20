# app.py

from flask import Flask, request, jsonify, render_template_string
from flask_mysqldb import MySQL
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

# Configure MySQL connection using variables from config.py
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print("Database connection successful")
        except Exception as e:
            print("Database connection failed: ", e)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Item added'}), 201
    else:
        form = '''
        <h1>Add New Item</h1>
        <form method="post" action="/">
            <label for="name">Item Name:</label>
            <input type="text" id="name" name="name">
            <input type="submit" value="Add Item">
        </form>
        '''
        return render_template_string(form)

# Route to create a new item
@app.route('/item', methods=['POST'])
def add_item():
    name = request.json['name']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Item added'}), 201

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    return jsonify(items)

# Route to get a single item
@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    return jsonify(item)

# Route to update an item
@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    name = request.json['name']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE items SET name = %s WHERE id = %s", (name, item_id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Item updated'})

# Route to delete an item
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

