from backend import get_db_connection 

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Handles database queries with optional fetching or committing."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)

        if commit:
            conn.commit()
            return None
        
        if fetchone:
            return cursor.fetchone()
        
        if fetchall:
            return cursor.fetchall()
