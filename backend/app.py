import os

import mysql.connector
import secrets
import string
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()


# =========================================================
# CONEXIÓN A MYSQL
# =========================================================

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


# =========================================================
# FLASK
# =========================================================


def generate_tracking_number():
    """
    Genera un código de rastreo único.

    Ejemplo:
    DT-2026-A7K92P
    """

    year = datetime.now().year

    characters = string.ascii_uppercase + string.digits

    random_code = ''.join(
        secrets.choice(characters)
        for _ in range(6)
    )

    return f"DT-{year}-{random_code}"






def create_app():

    app = Flask(__name__)

    # Permite que el frontend se comunique con Flask
    CORS(app)


    # =====================================================
    # INICIO
    # =====================================================

    @app.get("/")
    def index():

        return jsonify({
            "message": "API de DroneTrack funcionando",
            "health_check": "/api/health"
        })


    # =====================================================
    # HEALTH CHECK
    # =====================================================

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
                "details": str(error)
            }), 503

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # REGISTRO DE USUARIO
    # =====================================================

    @app.post("/api/auth/register")
    def register():

        connection = None
        cursor = None

        try:

            data = request.get_json()

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "No se recibieron datos."
                }), 400


            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            name = data.get("name")
            phone = data.get("phone")
            address = data.get("address")


            # ---------------------------------------------
            # VALIDACIÓN
            # ---------------------------------------------

            if not username or not email or not password or not name:

                return jsonify({
                    "status": "error",
                    "message": "username, email, password y name son obligatorios."
                }), 400


            if len(password) < 6:

                return jsonify({
                    "status": "error",
                    "message": "La contraseña debe tener al menos 6 caracteres."
                }), 400


            connection = get_database_connection()

            cursor = connection.cursor()


            # ---------------------------------------------
            # COMPROBAR SI YA EXISTE
            # ---------------------------------------------

            cursor.execute("""
                SELECT id
                FROM usuarios
                WHERE username = %s
                   OR email = %s
            """, (username, email))


            existing_user = cursor.fetchone()


            if existing_user:

                return jsonify({
                    "status": "error",
                    "message": "El usuario o correo ya está registrado."
                }), 409


            # ---------------------------------------------
            # GENERAR HASH
            # ---------------------------------------------

            password_hash = generate_password_hash(password)


            # ---------------------------------------------
            # CREAR USUARIO
            # ---------------------------------------------

            cursor.execute("""
                INSERT INTO usuarios (
                    username,
                    email,
                    password_hash
                )
                VALUES (%s, %s, %s)
            """, (
                username,
                email,
                password_hash
            ))


            user_id = cursor.lastrowid


            # ---------------------------------------------
            # CREAR CLIENTE
            # ---------------------------------------------

            cursor.execute("""
                INSERT INTO clientes (
                    user_id,
                    name,
                    phone,
                    address
                )
                VALUES (%s, %s, %s, %s)
            """, (
                user_id,
                name,
                phone,
                address
            ))


            connection.commit()


            return jsonify({
                "status": "ok",
                "message": "Usuario registrado correctamente.",
                "user_id": user_id
            }), 201


        except Error as error:

            if connection:
                connection.rollback()

            return jsonify({
                "status": "error",
                "message": "No fue posible registrar el usuario.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # LOGIN
    # =====================================================

    @app.post("/api/auth/login")
    def login():

        connection = None
        cursor = None

        try:

            data = request.get_json()

            if not data:

                return jsonify({
                    "status": "error",
                    "message": "No se recibieron datos."
                }), 400


            email = data.get("email")
            password = data.get("password")


            if not email or not password:

                return jsonify({
                    "status": "error",
                    "message": "Email y contraseña son obligatorios."
                }), 400


            connection = get_database_connection()

            cursor = connection.cursor(dictionary=True)


            cursor.execute("""
                SELECT
                    id,
                    username,
                    email,
                    password_hash
                FROM usuarios
                WHERE email = %s
            """, (email,))


            user = cursor.fetchone()


            if not user:

                return jsonify({
                    "status": "error",
                    "message": "Credenciales incorrectas."
                }), 401


            # ---------------------------------------------
            # COMPROBAR CONTRASEÑA
            # ---------------------------------------------

            if not check_password_hash(
                user["password_hash"],
                password
            ):

                return jsonify({
                    "status": "error",
                    "message": "Credenciales incorrectas."
                }), 401


            return jsonify({
                "status": "ok",
                "message": "Login correcto.",
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"]
                }
            })


        except Error as error:

            return jsonify({
                "status": "error",
                "message": "No fue posible realizar el login.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # OBTENER INFORMACIÓN DEL USUARIO
    # =====================================================

    @app.get("/api/usuarios/<int:user_id>")
    def get_usuario(user_id):

        connection = None
        cursor = None

        try:

            connection = get_database_connection()

            cursor = connection.cursor(dictionary=True)


            cursor.execute("""
                SELECT
                    u.id,
                    u.username,
                    u.email,
                    u.created_at,

                    c.name,
                    c.phone,
                    c.address

                FROM usuarios u

                INNER JOIN clientes c
                    ON u.id = c.user_id

                WHERE u.id = %s
            """, (user_id,))


            user = cursor.fetchone()


            if not user:

                return jsonify({
                    "status": "error",
                    "message": "Usuario no encontrado."
                }), 404


            return jsonify({
                "status": "ok",
                "user": user
            })


        except Error as error:

            return jsonify({
                "status": "error",
                "message": "No fue posible consultar el usuario.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # PAQUETES DE UN USUARIO
    # =====================================================

    @app.get("/api/usuarios/<int:user_id>/paquetes")
    def get_user_packages(user_id):

        connection = None
        cursor = None

        try:

            connection = get_database_connection()

            cursor = connection.cursor(dictionary=True)


            cursor.execute("""
                SELECT

                    p.id,
                    p.tracking_number,
                    p.origin,
                    p.destination,
                    p.weight_kg,
                    p.created_at,
                    p.estimated_delivery,
                    p.delivered_at,

                    ep.name AS estado,

                    d.drone_code AS drone

                FROM paquetes p

                INNER JOIN clientes c
                    ON p.client_id = c.id

                INNER JOIN estados_paquete ep
                    ON p.status_id = ep.id

                LEFT JOIN drones d
                    ON p.drone_id = d.id

                WHERE c.user_id = %s

                ORDER BY p.created_at DESC
            """, (user_id,))


            packages = cursor.fetchall()


            return jsonify({
                "status": "ok",
                "user_id": user_id,
                "packages": packages
            })


        except Error as error:

            return jsonify({
                "status": "error",
                "message": "No fue posible obtener los paquetes.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # TODOS LOS PAQUETES
    # =====================================================

    @app.get("/api/paquetes")
    def get_paquetes():

        connection = None
        cursor = None

        try:

            connection = get_database_connection()

            cursor = connection.cursor(dictionary=True)


            cursor.execute("""
                SELECT

                    p.id,
                    p.tracking_number,
                    p.origin,
                    p.destination,
                    p.weight_kg,
                    p.estimated_delivery,
                    p.delivered_at,

                    c.name AS cliente,

                    ep.name AS estado,

                    d.drone_code AS drone

                FROM paquetes p

                INNER JOIN clientes c
                    ON p.client_id = c.id

                INNER JOIN estados_paquete ep
                    ON p.status_id = ep.id

                LEFT JOIN drones d
                    ON p.drone_id = d.id

                ORDER BY p.id
            """)


            packages = cursor.fetchall()


            return jsonify(packages)


        except Error as error:

            return jsonify({
                "status": "error",
                "message": "No fue posible obtener los paquetes.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # OBTENER UN PAQUETE POR TRACKING NUMBER
    # =====================================================

    @app.get("/api/paquetes/<string:tracking_number>")
    def get_paquete(tracking_number):

        connection = None
        cursor = None

        try:

            connection = get_database_connection()

            cursor = connection.cursor(dictionary=True)


            cursor.execute("""
                SELECT

                    p.id,
                    p.tracking_number,
                    p.origin,
                    p.destination,
                    p.weight_kg,
                    p.estimated_delivery,
                    p.delivered_at,

                    c.name AS cliente,
                    c.phone AS cliente_phone,

                    ep.name AS estado,
                    ep.description AS estado_descripcion,

                    d.drone_code AS drone,
                    d.status AS drone_status,
                    d.battery_level AS drone_battery

                FROM paquetes p

                INNER JOIN clientes c
                    ON p.client_id = c.id

                INNER JOIN estados_paquete ep
                    ON p.status_id = ep.id

                LEFT JOIN drones d
                    ON p.drone_id = d.id

                WHERE p.tracking_number = %s
            """, (tracking_number,))


            package = cursor.fetchone()


            if not package:

                return jsonify({
                    "status": "error",
                    "message": "Paquete no encontrado.",
                    "tracking_number": tracking_number
                }), 404


            return jsonify({
                "status": "ok",
                "package": package
            })


        except Error as error:

            return jsonify({
                "status": "error",
                "message": "No fue posible consultar el paquete.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # =====================================================
    # CREAR PAQUETE Y GENERAR TRACKING NUMBER
    # =====================================================

    @app.post("/api/paquetes")
    def create_paquete():

        connection = None
        cursor = None

        try:

            data = request.get_json()

            if not data:

                return jsonify({
                    "status": "error",
                    "message": "No se recibieron datos."
                }), 400


            # ---------------------------------------------
            # DATOS RECIBIDOS
            # ---------------------------------------------

            user_id = data.get("user_id")
            origin = data.get("origin")
            destination = data.get("destination")
            weight_kg = data.get("weight_kg")
            estimated_delivery = data.get("estimated_delivery")


            # ---------------------------------------------
            # VALIDACIÓN
            # ---------------------------------------------

            if not user_id:
                return jsonify({
                    "status": "error",
                    "message": "user_id es obligatorio."
                }), 400


            if not origin or not destination or weight_kg is None:

                return jsonify({
                    "status": "error",
                    "message": "origin, destination y weight_kg son obligatorios."
                }), 400


            connection = get_database_connection()

            cursor = connection.cursor(dictionary=True)


            # ---------------------------------------------
            # OBTENER CLIENTE DEL USUARIO
            # ---------------------------------------------

            cursor.execute("""
                SELECT id
                FROM clientes
                WHERE user_id = %s
            """, (user_id,))


            client = cursor.fetchone()


            if not client:

                return jsonify({
                    "status": "error",
                    "message": "El usuario no tiene un cliente asociado."
                }), 404


            client_id = client["id"]


            # ---------------------------------------------
            # ESTADO INICIAL
            # ---------------------------------------------

            cursor.execute("""
                SELECT id
                FROM estados_paquete
                WHERE name = 'registered'
            """)


            status = cursor.fetchone()


            if not status:

                return jsonify({
                    "status": "error",
                    "message": "No existe el estado inicial 'registered'."
                }), 500


            status_id = status["id"]


            # ---------------------------------------------
            # GENERAR TRACKING NUMBER
            # ---------------------------------------------

            while True:

                tracking_number = generate_tracking_number()

                cursor.execute("""
                    SELECT id
                    FROM paquetes
                    WHERE tracking_number = %s
                """, (tracking_number,))

                existing_package = cursor.fetchone()

                if not existing_package:
                    break


            # ---------------------------------------------
            # CREAR PAQUETE
            # ---------------------------------------------

            cursor.execute("""
                INSERT INTO paquetes (
                    tracking_number,
                    client_id,
                    origin,
                    destination,
                    weight_kg,
                    status_id,
                    drone_id,
                    estimated_delivery
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    NULL,
                    %s
                )
            """, (
                tracking_number,
                client_id,
                origin,
                destination,
                weight_kg,
                status_id,
                estimated_delivery
            ))


            package_id = cursor.lastrowid


            # ---------------------------------------------
            # CREAR PRIMER REGISTRO DEL HISTORIAL
            # ---------------------------------------------

            cursor.execute("""
                INSERT INTO historial_paquete (
                    package_id,
                    status_id,
                    location,
                    comment
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                package_id,
                status_id,
                origin,
                "Paquete registrado."
            ))


            connection.commit()


            # ---------------------------------------------
            # RESPUESTA
            # ---------------------------------------------

            return jsonify({
                "status": "ok",
                "message": "Paquete creado correctamente.",
                "package": {
                    "id": package_id,
                    "tracking_number": tracking_number,
                    "client_id": client_id,
                    "origin": origin,
                    "destination": destination,
                    "weight_kg": weight_kg,
                    "status": "registered"
                }
            }), 201


        except Error as error:

            if connection:
                connection.rollback()

            return jsonify({
                "status": "error",
                "message": "No fue posible crear el paquete.",
                "details": str(error)
            }), 500


        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return app


# =========================================================
# EJECUTAR SERVIDOR
# =========================================================

if __name__ == "__main__":

    app = create_app()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
