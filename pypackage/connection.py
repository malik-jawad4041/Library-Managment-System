import psycopg2 as pg
import dotenv as env
import os
import logging

logging.basicConfig(filename="logger.txt",level=logging.INFO)
logger = logging.getLogger(__name__)
class con:

    variables = False
    @classmethod
    def connect(cls):
        '''FOR DATA BASE CONNECTION'''


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
            logger.info("Connection Established Successfully :)")
            return obj
        except pg.Error as err :
            logger.setLevel(logging.ERROR)
            print("ERROR:",err)
            logger.setLevel(logging.ERROR)


    @staticmethod
    def disconnect(connection):
        '''FOR DISCONNECTING FROM DATABASE'''
    
        if connection:
            connection.close()
        
        else:
            logging.info("There is no connection!")


