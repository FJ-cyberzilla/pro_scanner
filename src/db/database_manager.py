import aiosqlite
import logging
from typing import Optional, Dict, List, Any

# Configure logging for the database manager
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages all database operations for the ProScanner application.
    Uses aiosqlite for an asynchronous interface with an SQLite database.
    """
    
    DB_NAME = "pro_scanner.db"

    # Define the database schema using multiline strings
    CREATE_SESSIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS scan_sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        username_scanned TEXT NOT NULL,
        results_count INTEGER,
        duration REAL
    );
    """

    CREATE_RESULTS_TABLE = """
    CREATE TABLE IF NOT EXISTS scan_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        site_name TEXT NOT NULL,
        status TEXT NOT NULL,
        full_name TEXT,
        followers INTEGER,
        following INTEGER,
        posts INTEGER,
        is_private BOOLEAN,
        is_verified BOOLEAN,
        FOREIGN KEY (session_id) REFERENCES scan_sessions (session_id)
    );
    """
    
    def __init__(self):
        # We don't open the connection here, only when a method is called.
        self._conn = None

    async def _get_conn(self) -> aiosqlite.Connection:
        """Returns a single, shared connection instance."""
        if not self._conn:
            self._conn = await aiosqlite.connect(self.DB_NAME)
            await self._setup_tables()
        return self._conn

    async def _setup_tables(self):
        """Creates the necessary tables if they do not exist."""
        try:
            conn = await self._get_conn()
            await conn.execute(self.CREATE_SESSIONS_TABLE)
            await conn.execute(self.CREATE_RESULTS_TABLE)
            await conn.commit()
            logger.info("Database tables verified/created successfully.")
        except aiosqlite.Error as e:
            logger.error(f"Failed to create database tables: {e}")

    async def save_session(self, username: str, results_count: int, duration: float) -> Optional[int]:
        """Saves a new scan session to the database and returns its ID."""
        try:
            conn = await self._get_conn()
            timestamp = datetime.datetime.now().isoformat()
            query = "INSERT INTO scan_sessions (timestamp, username_scanned, results_count, duration) VALUES (?, ?, ?, ?);"
            cursor = await conn.execute(query, (timestamp, username, results_count, duration))
            await conn.commit()
            logger.info(f"Scan session saved for {username}.")
            return cursor.lastrowid
        except aiosqlite.Error as e:
            logger.error(f"Error saving scan session for {username}: {e}")
            return None

    async def save_result(self, session_id: int, site_name: str, status: str, details: Optional[Dict] = None):
        """Saves a single scan result linked to a session."""
        try:
            conn = await self._get_conn()
            
            # Prepare data for insertion
            full_name = details.get('full_name') if details else None
            followers = details.get('followers') if details else None
            following = details.get('following') if details else None
            posts = details.get('posts') if details else None
            is_private = details.get('is_private') if details else None
            is_verified = details.get('is_verified') if details else None

            query = """
            INSERT INTO scan_results (session_id, site_name, status, full_name, followers, following, posts, is_private, is_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            await conn.execute(query, (session_id, site_name, status, full_name, followers, following, posts, is_private, is_verified))
            await conn.commit()
            logger.info(f"Scan result saved for {site_name}.")
        except aiosqlite.Error as e:
            logger.error(f"Error saving scan result for {site_name}: {e}")

    async def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Retrieves a list of all past scan sessions."""
        try:
            conn = await self._get_conn()
            query = "SELECT * FROM scan_sessions ORDER BY timestamp DESC;"
            cursor = await conn.execute(query)
            sessions = await cursor.fetchall()
            return [dict(row) for row in sessions]
        except aiosqlite.Error as e:
            logger.error(f"Error retrieving sessions: {e}")
            return []

    async def close(self):
        """Closes the database connection if it's open."""
        if self._conn:
            await self._conn.close()
            self._conn = None
            logger.info("Database connection closed.")
