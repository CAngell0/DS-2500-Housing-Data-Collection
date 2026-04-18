# Author: Carson Angell
# Date: 4/14/2026

from typing import TypedDict, NotRequired, Unpack
import mysql.connector


# Type class used to document the kwargs in MySQLConnection
class ConnectionArgs(TypedDict):
    host: str
    """  Host of the database to connect to (e.g. 'my.database.com') """
    user: str
    """  Username of the user credentials to use for the database connection """
    password: str
    """  Password associated with the user to log into the database """
    database: NotRequired[str]
    """  Database to connect to inside the MySQL instance """



# A wrapper class used to interface with MySQL databases
class MySQLConnection:
    """
    A database wrapper class used to connect to MySQL databases and interact with them.
    """

    def __init__(self, **kwargs: Unpack[ConnectionArgs]) -> None:
        """
        Creates a new database connectio to a MySQL database. Make sure to provide necessary arguments to make the connection
        """

        # Get the kwargs values and put them in the input kwargs for mysql.connector.connect()
        connection_kwargs = {
            'host': kwargs.get('host'),
            'user': kwargs.get('user'),
            'password': kwargs.get('password')
        }
        
        # If a database was specified, put it in the connection_kwargs
        if (kwargs.get('database') != None): connection_kwargs['database'] = str(kwargs.get('database'))

        # Start the connection to the database
        print( '\t- Connecting to MySQL database...' )
        self.db = mysql.connector.connect(**connection_kwargs)

        if self.db.is_connected():
            print( '\t- Successfully connected' )
        else:
            raise Exception('Could not connect to database, check environment variables and try again.')
        
        self.cursor = self.db.cursor()
    


    def send(self, query: str) -> list[str]:
        """
        Sends an SQL query to the database and returns the resulting data.

        :param query: SQL query to send to the database
        :return: A list containing all the lines of the resulting data.
        :rtype: list[str]
        """

        data = []
        self.cursor.execute(query)
        self.db.commit()

        for row in self.cursor.fetchall():
            data.append(row)
        
        return data
