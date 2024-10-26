import sqlite3

# Database setup
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    sql_create_sessions_table = """ CREATE TABLE IF NOT EXISTS user_sessions (
                                        user_id TEXT PRIMARY KEY,
                                        last_message TEXT
                                    ); """
    conn.execute(sql_create_sessions_table)

def add_or_update_user_session(conn, user_id, message):
    sql = """ INSERT OR REPLACE INTO user_sessions (user_id, last_message) 
              VALUES (?, ?) """
    conn.execute(sql, (user_id, message))
    conn.commit()

def get_user_session(conn, user_id):
    sql = "SELECT last_message FROM user_sessions WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

# Example usage
if __name__ == '__main__':
    conn = create_connection('user_sessions.db')
    create_table(conn)
    conn.close()
