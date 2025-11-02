"""
Database Migration: Add Fraud Detection Fields
===============================================
Adds ML-powered fraud detection fields to the users table.

New fields:
- risk_score: Float (0.0-1.0) - ML model's fraud probability
- is_suspicious: Boolean - Flagged for admin review
- fraud_reason: String - Decision reason (auto-allow, auto-review-required, auto-block-recommended)
- fraud_checked_at: DateTime - When fraud check was performed
- fraud_reviewed_by: Integer - Admin ID who reviewed the account
- fraud_review_note: String - Admin's review notes
"""

import os
import sys
from sqlalchemy import text

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import User

def run_migration():
    with app.app_context():
        print("\n" + "="*60)
        print("FRAUD DETECTION FIELDS MIGRATION")
        print("="*60)
        print("This will add ML fraud detection fields to the users table.")
        print()
        
        confirm = input("Proceed with migration? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Migration cancelled.")
            return
        
        try:
            print("\n[1/3] Checking current database schema...")
            
            # Check if fields already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            fraud_fields = ['risk_score', 'is_suspicious', 'fraud_reason', 
                          'fraud_checked_at', 'fraud_reviewed_by', 'fraud_review_note']
            existing_fraud_fields = [f for f in fraud_fields if f in columns]
            
            if existing_fraud_fields:
                print(f"WARNING: Some fraud fields already exist: {existing_fraud_fields}")
                print("Skipping migration for existing fields.")
                if len(existing_fraud_fields) == len(fraud_fields):
                    print("All fraud fields already exist. Migration not needed.")
                    return
            
            print(f"Current columns: {len(columns)}")
            print(f"Will add: {[f for f in fraud_fields if f not in columns]}")
            
            print("\n[2/3] Creating new table with fraud fields...")
            
            # SQLite migration: create new table, copy data, replace old table
            with db.engine.begin() as connection:
                connection.execute(text("PRAGMA foreign_keys=OFF;"))
                
                # Create new table with all fields including fraud detection
                connection.execute(text("""
                    CREATE TABLE users_new (
                        id INTEGER NOT NULL PRIMARY KEY,
                        email VARCHAR(120) NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        created_at DATETIME NOT NULL,
                        username VARCHAR(80),
                        full_name VARCHAR(150),
                        role VARCHAR(20) NOT NULL,
                        permissions VARCHAR(500),
                        is_verified BOOLEAN,
                        verification_code VARCHAR(6),
                        verification_sent_at DATETIME,
                        risk_score FLOAT,
                        is_suspicious BOOLEAN DEFAULT 0,
                        fraud_reason VARCHAR(255),
                        fraud_checked_at DATETIME,
                        fraud_reviewed_by INTEGER,
                        fraud_review_note VARCHAR(500),
                        UNIQUE(email, role)
                    );
                """))
                
                # Copy existing data
                print("Copying existing user data...")
                connection.execute(text("""
                    INSERT INTO users_new 
                    (id, email, password_hash, name, created_at, username, full_name, 
                     role, permissions, is_verified, verification_code, verification_sent_at,
                     risk_score, is_suspicious, fraud_reason, fraud_checked_at, fraud_reviewed_by, fraud_review_note)
                    SELECT 
                        id, email, password_hash, name, created_at, username, full_name,
                        role, permissions, is_verified, verification_code, verification_sent_at,
                        NULL, 0, NULL, NULL, NULL, NULL
                    FROM users;
                """))
                
                # Replace old table
                connection.execute(text("DROP TABLE users;"))
                connection.execute(text("ALTER TABLE users_new RENAME TO users;"))
                
                # Recreate indexes
                print("Creating indexes...")
                connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS ix_users_risk_score ON users(risk_score);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS ix_users_is_suspicious ON users(is_suspicious);"))
                
                connection.execute(text("PRAGMA foreign_keys=ON;"))
            
            print("\n[3/3] Verifying migration...")
            
            # Verify new columns exist
            inspector = db.inspect(db.engine)
            new_columns = [col['name'] for col in inspector.get_columns('users')]
            
            print(f"Total columns after migration: {len(new_columns)}")
            
            # Check all fraud fields are present
            missing = [f for f in fraud_fields if f not in new_columns]
            if missing:
                print(f"ERROR: Some fields are missing: {missing}")
                return
            
            print("\n" + "="*60)
            print("MIGRATION COMPLETED SUCCESSFULLY")
            print("="*60)
            print("\nFraud detection fields added:")
            for field in fraud_fields:
                print(f"  - {field}")
            print("\nNew features:")
            print("  - ML-powered fraud scoring on signup")
            print("  - Admin review queue for suspicious accounts")
            print("  - Fraud statistics and monitoring")
            print("="*60)
            
        except Exception as e:
            db.session.rollback()
            print(f"\nERROR during migration: {e}")
            print("Migration failed. Database might be in an inconsistent state.")
            import traceback
            traceback.print_exc()
        finally:
            db.session.close()

if __name__ == '__main__':
    run_migration()

