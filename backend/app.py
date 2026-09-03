import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request
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

    # ---------------------------------------------------------
    # RUTA PRINCIPAL
    # ---------------------------------------------------------

    @app.get("/")
    def index():
        return jsonify({
            "message": "API de DroneTrack funcionando",
            "health_check": "/api/health",
        })

    # ---------------------------------------------------------
    # HEALTH CHECK
    # ---------------------------------------------------------

    @app.get("/api/health")
    def health_check():
        connection = None
        cursor = None

        try:
            connection = get_database_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT DATABASE()")
            database_name = cursor.fetchone()[0]

            return jsonify({
                "status": "ok",
                "database": database_name
            })

        except Error as error:
            return jsonify({
                "status": "error",
                "message": "No fue posible conectar con MySQL.",
                "details": str(error),
            }), 503

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ---------------------------------------------------------
    # OBTENER TODOS LOS DRONES
    # ---------------------------------------------------------

    @app.get("/api/drones")
    def get_drones():
        connection = None
        cursor = None

        try:
            connection = get_database_connection()

            # dictionary=True hace que cada fila sea un diccionario
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    drone_code,
                    status,
                    battery_level,
                    created_at
                FROM drones
                ORDER BY id
            """)

            drones = cursor.fetchall()

            return jsonify({
                "status": "ok",
                "count": len(drones),
                "drones": drones
            })

        except Error as error:
            return jsonify({
                "status": "error",
                "message": "No fue posible obtener los drones.",
                "details": str(error),
            }), 500

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ---------------------------------------------------------
    # OBTENER UN DRON POR ID
    # ---------------------------------------------------------

    @app.get("/api/drones/<int:drone_id>")
    def get_drone(drone_id):
        connection = None
        cursor = None

        try:
            connection = get_database_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    drone_code,
                    status,
                    battery_level,
                    created_at
                FROM drones
                WHERE id = %s
            """, (drone_id,))

            drone = cursor.fetchone()

            if drone is None:
                return jsonify({
                    "status": "error",
                    "message": "Dron no encontrado."
                }), 404

            return jsonify({
                "status": "ok",
                "drone": drone
            })

        except Error as error:
            return jsonify({
                "status": "error",
                "message": "Error al consultar el dron.",
                "details": str(error),
            }), 500

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ---------------------------------------------------------
    # CREAR UN DRON
    # ---------------------------------------------------------

    @app.post("/api/drones")
    def create_drone():
        connection = None
        cursor = None

        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "No se recibió información."
                }), 400

            drone_code = data.get("drone_code")
            status = data.get("status", "available")
            battery_level = data.get("battery_level", 100)

            if not drone_code:
                return jsonify({
                    "status": "error",
                    "message": "drone_code es obligatorio."
                }), 400

            connection = get_database_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO drones
                    (drone_code, status, battery_level)
                VALUES
                    (%s, %s, %s)
            """, (
                drone_code,
                status,
                battery_level
            ))

            connection.commit()

            new_drone_id = cursor.lastrowid

            return jsonify({
                "status": "ok",
                "message": "Dron creado correctamente.",
                "id": new_drone_id,
                "drone_code": drone_code
            }), 201

        except Error as error:
            if connection:
                connection.rollback()

            return jsonify({
                "status": "error",
                "message": "No fue posible crear el dron.",
                "details": str(error),
            }), 500

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ---------------------------------------------------------
    # ACTUALIZAR ESTADO Y BATERÍA DE UN DRON
    # ---------------------------------------------------------

    @app.put("/api/drones/<int:drone_id>")
    def update_drone(drone_id):
        connection = None
        cursor = None

        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "No se recibió información."
                }), 400

            status = data.get("status")
            battery_level = data.get("battery_level")

            if status is None or battery_level is None:
                return jsonify({
                    "status": "error",
                    "message": "status y battery_level son obligatorios."
                }), 400

            connection = get_database_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE drones
                SET
                    status = %s,
                    battery_level = %s
                WHERE id = %s
            """, (
                status,
                battery_level,
                drone_id
            ))

            connection.commit()

            if cursor.rowcount == 0:
                return jsonify({
                    "status": "error",
                    "message": "Dron no encontrado."
                }), 404

            return jsonify({
                "status": "ok",
                "message": "Dron actualizado correctamente."
            })

        except Error as error:
            if connection:
                connection.rollback()

            return jsonify({
                "status": "error",
                "message": "No fue posible actualizar el dron.",
                "details": str(error),
            }), 500

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return app


# ---------------------------------------------------------
# EJECUCIÓN
# ---------------------------------------------------------

app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
