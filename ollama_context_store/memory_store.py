import sqlite3
from datetime import datetime

print("✅ memory_store loaded successfully")


class MemoryStore:

    def __init__(self, db_name="agent_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
        """

        cursor.execute(query)

        conn.commit()
        conn.close()

    def store(self, role, content):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        query = """
        INSERT INTO memory (role, content, timestamp)
        VALUES (?, ?, ?)
        """

        cursor.execute(query, (role, content, str(datetime.now())))

        conn.commit()
        conn.close()

    def get_recent(self, limit=5):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        query = """
        SELECT role, content FROM memory
        ORDER BY id DESC
        LIMIT ?
        """

        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        conn.close()

        context = ""
        for role, content in reversed(rows):
            context += f"{role}: {content}\n"

        return context
    
    def clear(self):
      conn = sqlite3.connect(self.db_name)
      cursor = conn.cursor()

      cursor.execute("DELETE FROM memory")

      conn.commit()
      conn.close()