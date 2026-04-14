import os
import mysql.connector

from dotenv import load_dotenv

# Load environment variables
load_dotenv();

class MySQLConnection:
    """
    A database wrapper class used to connect to MySQL databases and interact with them.
    """

    def __init__(self):
        """
        Creates a new database connectio to a MySQL database. Uses the following environment variables to make the
        connection:

        - DB_HOST -> Host of the database to connect to (e.g. 'my.database.com')
        - DB_USER -> Username of the user credentials to use for the database connection
        - DB_PASSWORD -> Password associated with the user to log into the database
        - DB_DATABASE -> Database to connect to inside the MySQL instance

        """

        print( 'Making connection to MySQL database..' )
        self.db = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_DATABASE')
        )

        if self.db.is_connected():
            print( 'Successfully connected' )
        else:
            raise Exception('Could not connect to database, check environment variables and try again.')
        
        self.cursor = self.db.cursor()
    


    def send(self, query: str) -> list[str]:
        """
        Sends an SQL query to the database and returns the resulting data.

        :param query: SQL query to send to the database
        :return: A list containg all the lines of the resulting data.
        :rtype: list[str]
        """

        data = []
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            data.append(row)
        
        return data
