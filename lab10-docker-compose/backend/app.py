from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask Backend!"

@app.route('/data')
def get_data():
    connection = None

    try:
        connection = mysql.connector.connect(
            host="database",
            user="root",
            password="rootpassword",
            database="mydb"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 'Hello from my NEW MySQL!' AS message;")
        result = cursor.fetchone()
        cursor.close()

        return jsonify({"message": result[0]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
