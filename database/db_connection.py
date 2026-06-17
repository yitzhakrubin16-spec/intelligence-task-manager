import mysql.connector

class DB_connection:
    def __init__(self, config: dict = {"host":"localhost",
                                 "port": 3306,
                                 "user": "root",
                                 "password":"1234",
                                 "database":"Intelligence_db"}):
        self.config = config

        self._connection = None

    def get_connection(self):
        if self._connection:
            return self._connection
        
        self._connection = mysql.connector.connect(**self.config)
        
        return self._connection

    def create_database(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db;")

        connection.commit()
        cursor.close()
        return
    
    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""CREATE TABLE IF NOT EXISTS agents
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        specialty VARCHAR(255) NOT NULL,
                        is_active BOOL DEFAULT TRUE,
                        completed_missions INT DEFAULT 0,
                        failed_missions INT DEFAULT 0,
                        agent_rank ENUM('Junior','Senior','Commander') NOT NULL);""")
       
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT(65535) NOT NULL,
                        location VARCHAR(255) NOT NULL,
                        difficulty INT NOT NULL,
                        importance INT NOT NULL,
                        status VARCHAR(255) DEFAULT "NEW",
                        risk_level VARCHAR(255) NOT NULL,
                        assigned_agent_id INT DEFAULT NULL);""")

        connection.commit()
        cursor.close()
        return

