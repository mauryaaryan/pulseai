import os
import sqlite3
from sqlite3 import Error
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_db_connection(db_file='voice_agent.db'):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row # enable column access by name
        return conn
    except Error as e:
        logger.error(f"Error connecting to database: {e}")
    
    return conn

def init_db(db_uri):
    """Initialize the database schema."""
    db_file = db_uri.replace('sqlite:///', '') if db_uri.startswith('sqlite:///') else db_uri
    conn = get_db_connection(db_file)
    if conn:
        try:
            schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'schema.sql')
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            logger.info("Database initialized successfully.")
        except FileNotFoundError:
            logger.warning("database/schema.sql not found. Make sure to create the schema if tables don't exist.")
        except Error as e:
            logger.error(f"Error executing schema: {e}")
        finally:
            conn.close()
