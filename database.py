import mysql.connector
from config import HOST, USERNAME, PASSWORD, DATABASE_NAME
import time


def get_db_connection():
    start = time.time()
    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE_NAME,
    )
    cursor = connection.cursor(dictionary=True)
    time_taken = time.time() - start
    print(f"Connection took: {time_taken:.2f} seconds")
    return connection, cursor


def get_records(requisition_number, connection, cursor):
    start = time.time()
    cursor.execute(
        "SELECT VISITORNAME FROM visitor_request WHERE REQUISITIONNO = %s",
        (requisition_number,),
    )
    name = cursor.fetchone()["VISITORNAME"]
    cursor.execute("SELECT * FROM visitor_request WHERE VISITORNAME = %s", (name,))
    records = cursor.fetchall()
    time_taken = time.time() - start
    print(f"Query took: {time_taken:.2f} seconds")
    return records