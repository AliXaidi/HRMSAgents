import pyodbc
from core.config import DB_CONNECTION_STRING

def execute_query(query, params=None, fetch=False):
    with pyodbc.connect(DB_CONNECTION_STRING) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        if fetch:
            return cursor.fetchall()
        conn.commit()
