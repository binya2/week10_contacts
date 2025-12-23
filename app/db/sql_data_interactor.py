import mysql.connector

from app.models import Contact


class MySQLConnector:
    def __init__(self, host, user, password=None, sql_file=""):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
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
                self.cursor.execute(command)
            except mysql.connector.Error as err:
                print(f"Command error:\n{command}\n{err}")
        self.connection.commit()


class MySQLContactRepository:
    def __init__(self, db: MySQLConnector):
        self.db: MySQLConnector = db

    def create_contact(self, contact: Contact) -> int:
        query = f"""
        INSERT INTO contact (first_name, last_name,phone_number)
        VALUES ({contact.first_name},{contact.last_name},{contact.phone_number});
        """
        cursor = self.db.cursor
        cursor.execute(query)
        self.db.connection.commit()
        if cursor.rowcount != 1:
            raise Exception("Insert failed")
        return cursor.lastrowid

    def get_contact_by_id(self, user_id):
        query = f"""
        SELECT * 
        FROM contact 
        WHERE id={user_id}"""
        self.get_contact_query(query)

    def get_contact_query(self, query):
        cursor = self.db.cursor
        cursor.execute(query)
        return cursor.fetchone()

    def get_all_contact(self):
        query = f"""
        SELECT * 
        FROM contact 
        """
        self.get_contact_query(query)
