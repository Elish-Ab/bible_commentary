from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# SQLite database setup
DATABASE = 'user_sessions.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            user_id TEXT PRIMARY KEY,
            last_message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Placeholder function to simulate model predictions
def generate_placeholder_commentary(verse):
    return {
        "geographical": f"Geographical context for {verse}.",
        "historical": f"Historical background for {verse}.",
        "theological": f"Theological insights for {verse}."
    }

class RequestData(BaseModel):
    verse: str
    user_id: str

@app.post("/generate_commentary")
async def generate_commentary(data: RequestData):
    # Store the user session in the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO sessions (user_id, last_message) VALUES (?, ?)
    ''', (data.user_id, data.verse))
    conn.commit()

    # Use the placeholder function for commentary
    commentary = generate_placeholder_commentary(data.verse)

    conn.close()
    return {
        "geographical": commentary["geographical"],
        "historical": commentary["historical"],
        "theological": commentary["theological"]
    }  # Ensure the response has these keys

# Initialize the database
init_db()
