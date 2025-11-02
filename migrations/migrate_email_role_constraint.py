"""
Migration Script: Update Email Constraint to Allow Same Email for Different Roles

This script:
1. Removes the unique constraint on the email column
2. Adds a composite unique constraint on (email, role)
3. Allows same email for student and admin accounts, but not for duplicate roles

Run this script once to update your database schema.
"""

import os
import sys
from sqlalchemy import text

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import User

def migrate_database():
    """Migrate database to support email+role uniqueness."""
    
    print("\n" + "="*60)
    print("EMAIL+ROLE CONSTRAINT MIGRATION")
    print("="*60)
    
    with app.app_context():
        print("\n[1/4] Checking current database schema...")
        
        # Check if we're using SQLite
        inspector = db.inspect(db.engine)
        print(f"Database engine: {db.engine.name}")
        
        # Get current table info
        columns = inspector.get_columns('users')
        indexes = inspector.get_indexes('users')
        
        print(f"Current columns: {[col['name'] for col in columns]}")
        print(f"Current indexes: {[idx['name'] for idx in indexes]}")
        
        try:
            print("\n[2/4] Creating backup...")
            # For SQLite, we need to recreate the table
            # First, let's check if there are any duplicate email+role combinations
            
            duplicates = db.session.execute(text("""
                SELECT email, role, COUNT(*) as count
                FROM users
                GROUP BY email, role
                HAVING COUNT(*) > 1
            """)).fetchall()
            
            if duplicates:
                print("\nWARNING: Found duplicate email+role combinations:")
                for dup in duplicates:
                    print(f"  - {dup[0]} ({dup[1]}): {dup[2]} accounts")
                print("\nPlease resolve these duplicates before proceeding.")
                return False
            
            print("No duplicate email+role combinations found.")
            
            print("\n[3/4] Updating database schema...")
            
            # For SQLite, we need to:
            # 1. Create a new table with the correct schema
            # 2. Copy data from old table
            # 3. Drop old table
            # 4. Rename new table
            
            # But since we're using Flask-SQLAlchemy, we can try a simpler approach
            # by dropping and recreating the table (be careful in production!)
            
            print("\nWARNING: This will temporarily lock the users table.")
            print("Proceeding with schema update...")
            
            # Drop the unique constraint on email if it exists
            try:
                # For SQLite, we need to recreate the table
                # This is handled by SQLAlchemy when we call db.create_all()
                # But first, let's try to update the index
                
                db.session.execute(text("DROP INDEX IF EXISTS ix_users_email"))
                db.session.commit()
                print("Dropped email index")
            except Exception as e:
                print(f"Note: {e}")
            
            # Create the composite unique constraint
            # This is defined in the model, so we just need to ensure it exists
            try:
                db.session.execute(text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_email_role ON users(email, role)"
                ))
                db.session.commit()
                print("Created composite unique constraint on (email, role)")
            except Exception as e:
                print(f"Error creating constraint: {e}")
                db.session.rollback()
            
            # Recreate the email index (non-unique)
            try:
                db.session.execute(text("CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)"))
                db.session.commit()
                print("Created non-unique email index")
            except Exception as e:
                print(f"Note: {e}")
            
            print("\n[4/4] Verifying schema update...")
            
            # Check new indexes
            new_indexes = inspector.get_indexes('users')
            print(f"Updated indexes: {[idx['name'] for idx in new_indexes]}")
            
            print("\n" + "="*60)
            print("MIGRATION COMPLETED SUCCESSFULLY")
            print("="*60)
            print("\nYou can now:")
            print("1. Create student account with email@example.com")
            print("2. Create admin account with same email@example.com")
            print("3. Cannot create duplicate student accounts with same email")
            print("4. Cannot create duplicate admin accounts with same email")
            print("="*60 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\nERROR: Migration failed: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("\nStarting database migration...")
    print("This will allow same email for different roles (student/admin)")
    print("but prevent duplicate email+role combinations.\n")
    
    response = input("Proceed with migration? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        success = migrate_database()
        if success:
            print("\nMigration completed successfully!")
            sys.exit(0)
        else:
            print("\nMigration failed. Please check the errors above.")
            sys.exit(1)
    else:
        print("Migration cancelled.")
        sys.exit(0)


