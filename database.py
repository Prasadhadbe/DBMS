import mysql.connector
from mysql.connector import Error


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            port = 30306,
            user = "root",
            password = "Nerogod",
            database = "school")
        print("Connection to mysql successful")
    except Error as e:
        print(f"the error '{e}' occurred")

    return connection



def execute_query(connection, query, values=None):
    cursor = connection.cursor()
    try:
        if values:
            print(query)
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def fetch_query(connection, query, values=None):
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries
    result = None
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        result = cursor.fetchall()  # Use fetchall() to retrieve all rows
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()  # Always close the cursor to release resources
        return result

def create_student(connection, name, age, grade):
    query = f"INSERT INTO students (name, age, grade) VALUES ('{name}', {age}, '{grade}')"
    values = (name, age, grade)
    execute_query(connection, query, values)


def get_students(connection):
    query = "SELECT * FROM students"
    return fetch_query(connection, query)

def get_student_by_id(connection, student_id):
    query = f"SELECT * FROM students WHERE id = {student_id}"
    values = (student_id,)
    return fetch_query(connection, query, values)


def update_student(connection, student_id, name, age, grade):
    query = f"UPDATE students SET name = '{name}', age = {age}, grade = '{grade}' WHERE id = {student_id}"
    values = (name, age, grade, student_id)
    execute_query(connection, query, values)

def delete_student(connection, student_id):
    query = f"DELETE FROM students WHERE id = {student_id}"
    values = (student_id)
    execute_query(connection, query, values)


# In[ ]:




