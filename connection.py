import psycopg2


def get_connection():
    return psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='Duckbill#Postgres01',
        port='5433'
    )
