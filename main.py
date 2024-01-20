import mysql.connector
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )

        if connection.is_connected():
            print(f"Connected to MySQL Server: {os.getenv('DB_HOST')} | Database: {os.getenv('DB_DATABASE')}")
            return connection

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def execute_select_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            print(row)

        cursor.close()

    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")

def execute_delete_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Record deleted successfully.")

        cursor.close()

    except mysql.connector.Error as e:
        print(f"Error executing delete query: {e}")
        connection.rollback()

def send_line_notification(token, message):
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"message": message}

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            print("Line notification sent successfully.")
            return True
        else:
            print(f"Failed to send Line notification. Status code: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"Error sending Line notification: {e}")
        return False


if __name__ == "__main__":
    connection = connect_to_mysql()

    if connection:
        # Example SELECT query
        select_query = "SELECT * FROM tasks"
        execute_select_query(connection, select_query)

        # Example DELETE query
        # record_id_to_delete = 1  # Replace with the actual record ID to delete
        # delete_query = f"DELETE FROM tasks WHERE id = {record_id_to_delete}"
        # execute_delete_query(connection, delete_query)

        # Display remaining records after deletion
        # execute_select_query(connection, select_query)

        connection.close()
        print("Connection closed.")

        token = os.getenv("LINE_NOTIFY_TOKEN")
        message = "test"
        send_line_notification(token, message)