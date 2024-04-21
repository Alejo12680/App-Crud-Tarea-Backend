from pymysql import connect
from decouple import config

# La coneccion esta con variables de entorno .env


def get_connection():
    try:
        conn = connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB'),
        )

        return conn

    except Exception as error:
        print(error)

