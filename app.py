from flask import Flask, jsonify
from flask_mysqldb import MySQL
import os
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite el acceso desde cualquier origen solucionando el problema de CORS

# Configuración de la conexión a MySQL usando variables de entorno
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'world_data')
}

def get_db_connection():
    """Función para establecer conexión con la base de datos."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/api/countries', methods=['GET'])
def get_countries():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM countries")
    countries = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(countries)

@app.route('/test_db')
def test_db():
    connection = get_db_connection()
    if connection is None:
        return "Error connecting to database", 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return f"Database test successful: {result}"
    except Exception as e:
        return f"Error executing query: {e}", 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)