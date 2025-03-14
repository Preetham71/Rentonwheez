import mysql.connector
import mysql
class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Admin@123",
                database="rentwheelz"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connection successful")
        except mysql.connector.Error as e:
            print(f"Failed to connect to database: {e}")
            raise  # Raise the exception to prevent creating an invalid Database object

    def commit(self):
        if self.connection and self.connection.is_connected():
            self.connection.commit()

    def rollback(self):
        if self.connection and self.connection.is_connected():
            self.connection.rollback()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")

    def execute(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                raise Exception("No active database connection")
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            raise

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

# # Example usage
# if __name__ == "__main__":
#     try:
#         db = Database()
#         db.close()
#     except Exception as e:
#         print(f"Error: {e}")