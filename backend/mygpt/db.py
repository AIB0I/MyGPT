import sqlite3
import datetime
import uuid
import threading
from .utils import logger

class DB:
    """
    Thread-safe database class for managing sessions and messages.
    """
    _local = threading.local()

    def __init__(self, db_file):
        """
        Initialize the database connection.

        Args:
            db_file (str): Path to the SQLite database file.
        """
        self.db_file = db_file
        self._local.conn = None
        self._local.cursor = None
        logger.info(f"DB class initialized with database file: {db_file}")

    def _get_conn(self):
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_file)
            self._local.cursor = self._local.conn.cursor()
            logger.info(f"New database connection created in thread: {threading.get_ident()}")
        return self._local.conn, self._local.cursor

    def create_tables(self):
        """
        Create necessary tables if they don't exist.
        """
        conn, cursor = self._get_conn()
        logger.info("Creating tables if they don't exist")
        # Create sessions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (session_id)
        )
        ''')
        conn.commit()
        logger.info("Tables created successfully")

    def add_session(self, session_id, title):
        """
        Add a new session to the database.

        Args:
            session_id (str): Unique identifier for the session.
            title (str): Title of the session.

        Returns:
            str: The session_id of the newly created session.
        """
        conn, cursor = self._get_conn()
        logger.info(f"Creating new session with ID: {session_id}")
        cursor.execute('INSERT INTO sessions (session_id, title) VALUES (?, ?)', (session_id, title))
        conn.commit()
        logger.info(f"New session created: {session_id}")
        return session_id

    def add_message(self, session_id, role, content):
        """
        Add a new message to a session.

        Args:
            session_id (str): ID of the session to add the message to.
            role (str): Role of the message sender (e.g., 'user' or 'assistant').
            content (str): Content of the message.
        """
        conn, cursor = self._get_conn()
        message_id = str(uuid.uuid4())
        logger.info(f"Saving message for session {session_id}")
        cursor.execute('INSERT INTO messages (message_id, session_id, role, content) VALUES (?, ?, ?, ?)',
                            (message_id, session_id, role, content))
        conn.commit()
        logger.info(f"Message saved with ID: {message_id}")

    def get_session_history(self, session_id):
        """
        Retrieve the message history for a given session.

        Args:
            session_id (str): ID of the session to retrieve history for.

        Returns:
            list: List of tuples containing (role, content) for each message.
        """
        conn, cursor = self._get_conn()
        logger.info(f"Retrieving session history for session {session_id}")
        cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp', (session_id,))
        history = cursor.fetchall()
        logger.info(f"Retrieved {len(history)} messages for session {session_id}")
        return history

    def get_session_title(self, session_id):
        """
        Retrieve the title of a given session.

        Args:
            session_id (str): ID of the session to retrieve the title for.

        Returns:
            str: The title of the session, or None if not found.
        """
        conn, cursor = self._get_conn()
        logger.info(f"Retrieving title for session {session_id}")
        cursor.execute('SELECT title FROM sessions WHERE session_id = ?', (session_id,))
        result = cursor.fetchone()
        if result:
            logger.info(f"Title retrieved for session {session_id}")
        else:
            logger.warning(f"No title found for session {session_id}")
        return result[0] if result else None

    def get_all_sessions(self):
        """
        Retrieve all sessions from the database.

        Returns:
            list: List of tuples containing (session_id, title) for each session.
        """
        conn, cursor = self._get_conn()
        logger.info("Retrieving all sessions")
        cursor.execute('SELECT session_id, title FROM sessions ORDER BY created_at DESC')
        sessions = cursor.fetchall()
        logger.info(f"Retrieved {len(sessions)} sessions")
        return sessions

    def close(self):
        """
        Close the database connection for the current thread.
        """
        if hasattr(self._local, 'conn') and self._local.conn is not None:
            self._local.conn.close()
            self._local.conn = None
            self._local.cursor = None
            logger.info(f"Database connection closed for thread: {threading.get_ident()}")

    def check_session(self, session_id):
        """
        Check if a session with the given ID exists in the database.

        Args:
            session_id (str): ID of the session to check.

        Returns:
            bool: True if the session exists, False otherwise.
        """
        conn, cursor = self._get_conn()
        logger.info(f"Checking if session {session_id} exists")
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE session_id = ?', (session_id,))
        count = cursor.fetchone()[0]
        exists = count > 0
        logger.info(f"Session {session_id} exists: {exists}")
        return exists