import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

mydb = connect_to_database()
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM your_table")