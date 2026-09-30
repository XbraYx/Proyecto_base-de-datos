import os
import mysql.connector

def inicializar_base_datos():
    try:
        # 1. Conexión a tu servidor MySQL local
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",        # Cambia por tu usuario de MySQL
            password="telecom" # Cambia por tu contraseña de MySQL
        )
        cursor = conexion.cursor()

        # 2. Ruta dinámica para encontrar el archivo SQL
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        
        # Asegúrate de que el nombre coincida exactamente con tu archivo (ej. schema.sql o schema2.sql)
        ruta_schema = os.path.join(ruta_actual, "schema2.sql")

        print(f"Leyendo archivo desde: {ruta_schema}")

        # 3. Leer el contenido del archivo SQL
        with open(ruta_schema, "r", encoding="utf-8") as archivo:
            sql_script = archivo.read()

        # 4. Dividir el script por cada punto y coma (;) para ejecutar las consultas una por una
        # Esto evita el error "Commands out of sync"
        sentencias = sql_script.split(';')

        for sentencia in sentencias:
            # Limpiar espacios en blanco o saltos de línea sobrantes
            sentencia_limpia = sentencia.strip()
            if sentencia_limpia:  # Si no está vacía, la ejecutamos
                cursor.execute(sentencia_limpia)

        conexion.commit()
        cursor.close()
        conexion.close()
        print("¡Base de datos y tablas creadas exitosamente desde el archivo SQL!")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    inicializar_base_datos()