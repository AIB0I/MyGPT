import sqlite3
import datetime
import uuid

class ChatDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
        )
        ''')
        self.conn.commit()

    def create_new_chat(self, title):
        chat_id = str(uuid.uuid4())
        self.cursor.execute('INSERT INTO chats (chat_id, title) VALUES (?, ?)', (chat_id, title))
        self.conn.commit()
        return chat_id

    def save_message(self, chat_id, role, content):
        message_id = str(uuid.uuid4())
        self.cursor.execute('INSERT INTO messages (message_id, chat_id, role, content) VALUES (?, ?, ?, ?)',
                            (message_id, chat_id, role, content))
        self.conn.commit()

    def get_chat_history(self, chat_id):
        self.cursor.execute('SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp', (chat_id,))
        return self.cursor.fetchall()

    def get_chat_title(self, chat_id):
        self.cursor.execute('SELECT title FROM chats WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_chats(self):
        self.cursor.execute('SELECT chat_id, title FROM chats ORDER BY created_at DESC')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()