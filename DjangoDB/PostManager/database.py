import psycopg2
from configparser import ConfigParser

class Database:
    __filename = None
    __section = None
    __config = None
    __connection = None
    cursor = None

    #loads database details from file
    def __getconfig(self, section, filename):
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        print("[OK] Configuration loaded!")
        return db

    #connects to database based on params
    def connect(self, DB_TYPE, DB_NAME, DB_IP, DB_PORT, DB_USERNAME, DB_PASSWORD):
        self.__connection = psycopg2.connect(
            database=DB_NAME,
            host=DB_IP,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )

        if (self.__connection):
            print("[OK] Connection established!")
            self.cursor = self.__connection.cursor()
            return
        print("[ERROR] Connection not created!")

    def connectConfig(self, DB_TYPE, CONF_FILE):
        config = self.__getconfig(DB_TYPE, CONF_FILE)
        self.__connection = psycopg2.connect(**config)
        if(self.__connection):
            self.cursor = self.__connection.cursor()
            print("[OK] Connection established!")
        print("[ERROR] Connection not created!")

    #executes raw SQL code
    def execute(self, sqlCommand):
        if(self.cursor):
            self.cursor.execute(sqlCommand)
            return self.cursor.fetchall()[0][0]
        return None

    #same as execute but more 'raw'
    def executeRaw(self, sqlCommand):
        if(self.cursor):
            self.cursor.execute(sqlCommand)
            return self.cursor.fetchall()


