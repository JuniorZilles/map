import psycopg2 # conexao com o postgres
import config

def get_database_rows(query):
    conn = None
    db_result = None
    try:
        params = config.get_db_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        db_result = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return db_result