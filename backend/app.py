import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify
from mysql.connector import Error

load_dotenv()


def get_database_connection():
    """Crea una conexión usando las variables definidas en .env."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "rastreador_drones"),
        connection_timeout=5,
    )


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify({
            "message": "API de DroneTrack funcionando",
            "health_check": "/api/health",
        })

    @app.get("/api/health")
    def health_check():
        connection = None
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            database_name = cursor.fetchone()[0]
            cursor.close()
            return jsonify({"status": "ok", "database": database_name})
        except Error as error:
            return jsonify({
                "status": "error",
                "message": "No fue posible conectar con MySQL.",
                "details": str(error),
            }), 503
        finally:
            if connection and connection.is_connected():
                connection.close()

    return app