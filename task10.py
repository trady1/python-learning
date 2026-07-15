from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello from my Flask server!"


@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    users_list = []
    for row in rows:
        users_list.append({'id': row[0], 'name': row[1], 'age': row[2]})

    return jsonify(users_list)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User added successfully!'}), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User deleted successfully!'}), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name =?, age =? WHERE id = ?", (name, age, user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User updated successfully!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
