import psycopg2 as pg
import dotenv as env
import os



class EXE(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class con:

    variables = False
    @classmethod
    def connect(cls):


        if(cls.variables == False):
            env.load_dotenv()
            variables = True
            cls.host = os.getenv("DB_HOST")
            cls.database = os.getenv("DB_NAME")
            cls.user = os.getenv("DB_USER")
            cls.password = os.getenv("PASSWORD")
            cls.port = os.getenv("DB_PORT")

        try:
            obj = pg.connect(
            host=cls.host,
            database=cls.database,
            user=cls.user,         # user is superuser postgres
            password=cls.password,
            port=cls.port
            )
            print("Connection Established Successfully :)")
            return obj
        except pg.Error as err :
            print("ERROR:",err)



    @staticmethod
    def disconnect(connection):
    
        if connection:
            connection.close()
        
        else:
            print("There is no connection!")


