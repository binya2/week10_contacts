import mysql.connector


class DatabaseConnector:

    def __init__(self, host, user, database, password=None, sql_file=""):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
        }
        self.connection = None
        self.cursor = None
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Connection to MySQL DB successful")
                if sql_file != "":
                    self.init_database(sql_file)
            else:
                raise ValueError("Connection to MySQL DB failed")
        except Exception as e:
            print(f"The error '{e}' occurred")

    def init_database(self, sql_file):
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

        for command in commands:
            try:
                self.execute_query(command)
            except mysql.connector.Error as err:
                print(f"Command error:\n{command}\n{err}")
        self.connection.commit()

    def execute_query(self, query):
        results = None
        try:
            if self.connection.is_connected():
                self.cursor.execute(query)
                query_type = query.strip().upper().split()[0]
                if query_type in ['INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']:
                    self.connection.commit()
                    results = self.cursor.rowcount
                    print(f"Query successful. {results} rows affected.")
                else:
                    results = self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            results = None

        return results
