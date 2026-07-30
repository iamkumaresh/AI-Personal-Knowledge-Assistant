import sqlite3
import json
import datetime
from typing import List, Dict, Any, Optional
from utils.config import DATABASE_PATH

def get_connection():
    """Create and return a database connection, allowing dict-like row access."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Documents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE NOT NULL,
        file_path TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        page_count INTEGER NOT NULL,
        char_count INTEGER NOT NULL,
        chunk_count INTEGER NOT NULL
    )
    """)
    
    # 2. Chat Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    # 3. Chat Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        sender TEXT NOT NULL, -- 'user' or 'ai'
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        sources TEXT, -- JSON string containing source file names and page numbers
        FOREIGN KEY (session_id) REFERENCES chat_sessions (id) ON DELETE CASCADE
    )
    """)
    
    # 4. Indexes for performance optimization
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_session ON chat_messages(session_id)")
    
    conn.commit()
    conn.close()

# --- DOCUMENT METADATA CRUD ---

def add_document(filename: str, file_path: str, page_count: int, char_count: int, chunk_count: int) -> bool:
    """Insert document metadata into database. If already exists, overwrite metadata."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute("""
        INSERT OR REPLACE INTO documents (filename, file_path, upload_date, page_count, char_count, chunk_count)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (filename, file_path, now, page_count, char_count, chunk_count))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding document metadata: {e}")
        return False

def delete_document(filename: str) -> bool:
    """Delete document metadata from database by filename."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE filename = ?", (filename,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting document metadata: {e}")
        return False

def get_all_documents() -> List[Dict[str, Any]]:
    """Retrieve all uploaded documents metadata."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents ORDER BY upload_date DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error reading documents: {e}")
        return []

def get_stats() -> Dict[str, Any]:
    """Retrieve aggregate project stats for the Home Dashboard."""
    stats = {
        "total_documents": 0,
        "total_pages": 0,
        "total_queries": 0
    }
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Count documents and sum pages
        cursor.execute("SELECT COUNT(*), SUM(page_count) FROM documents")
        doc_count, page_sum = cursor.fetchone()
        stats["total_documents"] = doc_count or 0
        stats["total_pages"] = page_sum or 0
        
        # Count user queries
        cursor.execute("SELECT COUNT(*) FROM chat_messages WHERE sender = 'user'")
        query_count = cursor.fetchone()[0]
        stats["total_queries"] = query_count or 0
        
        conn.close()
    except Exception as e:
        print(f"Error fetching stats: {e}")
    return stats

# --- CHAT SESSION & HISTORY TRACKING ---

def create_chat_session(session_id: str, title: str) -> bool:
    """Create a new chat session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute("""
        INSERT INTO chat_sessions (id, title, created_at)
        VALUES (?, ?, ?)
        """, (session_id, title, now))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating chat session: {e}")
        return False

def get_chat_sessions() -> List[Dict[str, Any]]:
    """Get all chat sessions, ordered by creation date."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_sessions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error getting sessions: {e}")
        return []

def add_chat_message(session_id: str, sender: str, message: str, sources: Optional[List[Dict[str, Any]]] = None) -> bool:
    """Log a new chat message to a session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        sources_json = json.dumps(sources) if sources else None
        
        cursor.execute("""
        INSERT INTO chat_messages (session_id, sender, message, timestamp, sources)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, sender, message, now, sources_json))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error logging chat message: {e}")
        return False

def get_chat_history(session_id: str) -> List[Dict[str, Any]]:
    """Retrieve full chat history for a session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT sender, message, timestamp, sources 
        FROM chat_messages 
        WHERE session_id = ? 
        ORDER BY id ASC
        """, (session_id,))
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            msg = dict(row)
            if msg["sources"]:
                try:
                    msg["sources"] = json.loads(msg["sources"])
                except Exception:
                    msg["sources"] = []
            else:
                msg["sources"] = []
            history.append(msg)
        return history
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []

def clear_chat_history(session_id: str) -> bool:
    """Delete all messages for a specific session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        return False

def delete_chat_session(session_id: str) -> bool:
    """Delete a chat session and all its messages."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting chat session: {e}")
        return False

# Auto-initialize database tables on module import
try:
    init_db()
except Exception as e:
    print(f"Database auto-init warning: {e}")
