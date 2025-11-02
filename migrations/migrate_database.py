"""
Database migration script to add conversation_id and chat_title columns
"""

import sqlite3
import os

DB_PATH = "instance/course_recommendation.db"

def migrate_database():
    """Add new columns to chat_history table if they don't exist."""
    
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(chat_history)")
        columns = [row[1] for row in cursor.fetchall()]
        
        migrations_applied = []
        
        # Add conversation_id column if it doesn't exist
        if 'conversation_id' not in columns:
            print("Adding conversation_id column...")
            cursor.execute("ALTER TABLE chat_history ADD COLUMN conversation_id VARCHAR(36)")
            migrations_applied.append("conversation_id")
        
        # Add chat_title column if it doesn't exist
        if 'chat_title' not in columns:
            print("Adding chat_title column...")
            cursor.execute("ALTER TABLE chat_history ADD COLUMN chat_title VARCHAR(255)")
            migrations_applied.append("chat_title")
        
        # Create index on conversation_id
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversation_id ON chat_history(conversation_id)")
            print("Index created on conversation_id")
        except Exception as e:
            print(f"Index might already exist: {e}")
        
        conn.commit()
        conn.close()
        
        if migrations_applied:
            print(f"Migration completed! Applied: {', '.join(migrations_applied)}")
        else:
            print("Database already up to date - all migrations applied.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting database migration...")
    migrate_database()
    print("Migration finished!")

