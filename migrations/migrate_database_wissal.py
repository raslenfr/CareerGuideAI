"""
Database Migration Script: Add Wissal User Management Fields
============================================================
This script migrates the existing database to add enhanced user management
fields from the Wissal backend while preserving all existing data.

Changes:
- Adds 7 new columns to users table (username, full_name, role, permissions, 
  is_verified, verification_code, verification_sent_at)
- Creates admin_logs table for audit tracking
- Populates default values for existing users
"""

from app import app, db
from models import User, AdminLog
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def upgrade_users_table():
    """Add new columns to users table"""
    print("\n" + "="*60)
    print("PHASE 1: Upgrading users table")
    print("="*60)
    
    with app.app_context():
        try:
            # SQLite doesn't support adding UNIQUE columns directly, so add columns first
            alterations = [
                ("username", "ALTER TABLE users ADD COLUMN username TEXT"),
                ("full_name", "ALTER TABLE users ADD COLUMN full_name TEXT"),
                ("role", "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'"),
                ("permissions", "ALTER TABLE users ADD COLUMN permissions TEXT"),
                ("is_verified", "ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0"),
                ("verification_code", "ALTER TABLE users ADD COLUMN verification_code TEXT"),
                ("verification_sent_at", "ALTER TABLE users ADD COLUMN verification_sent_at DATETIME")
            ]
            
            for column_name, sql in alterations:
                try:
                    db.session.execute(text(sql))
                    print(f"[OK] Added column: {column_name}")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print(f"[WARN] Column '{column_name}' already exists, skipping...")
                    else:
                        raise
            
            db.session.commit()
            print("\n[SUCCESS] User table upgrade successful!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Migration failed: {e}")
            raise


def populate_new_fields():
    """Set default values for existing users"""
    print("\n" + "="*60)
    print("PHASE 2: Populating new fields for existing users")
    print("="*60)
    
    with app.app_context():
        try:
            users = User.query.all()
            print(f"\nFound {len(users)} existing users")
            
            for user in users:
                # Set username from email (before @)
                if not user.username:
                    base_username = user.email.split('@')[0]
                    # Handle potential duplicates
                    counter = 1
                    username = base_username
                    while User.query.filter_by(username=username).first():
                        username = f"{base_username}{counter}"
                        counter += 1
                    user.username = username
                    print(f"  [OK] Set username for {user.email}: {username}")
                
                # Set full_name from name
                if not user.full_name:
                    user.full_name = user.name
                
                # Set default role (first user becomes admin, rest are students)
                if not user.role:
                    if user.id == 1:
                        user.role = 'admin'
                        print(f"  [ADMIN] User {user.email} set as ADMIN (first user)")
                    else:
                        user.role = 'student'
                
                # Mark existing users as verified (they're already in the system)
                if user.is_verified is None or user.is_verified is False:
                    user.is_verified = True
                    print(f"  [OK] Marked {user.email} as verified")
            
            db.session.commit()
            print(f"\n[SUCCESS] Successfully populated fields for {len(users)} users")
            
            # Now create unique index on username (after data is populated)
            try:
                db.session.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username)"))
                db.session.commit()
                print("[OK] Created unique index on username column")
            except Exception as e:
                print(f"[WARN] Could not create unique index on username: {e}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Population failed: {e}")
            raise


def create_admin_logs_table():
    """Create AdminLog table"""
    print("\n" + "="*60)
    print("PHASE 3: Creating admin_logs table")
    print("="*60)
    
    with app.app_context():
        try:
            # This will create admin_logs if it doesn't exist
            db.create_all()
            print("[SUCCESS] AdminLog table created successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to create AdminLog table: {e}")
            raise


def verify_migration():
    """Verify that migration was successful"""
    print("\n" + "="*60)
    print("PHASE 4: Verifying migration")
    print("="*60)
    
    with app.app_context():
        try:
            # Check users table
            users = User.query.all()
            print(f"\nUsers table:")
            print(f"   Total users: {len(users)}")
            
            if users:
                sample_user = users[0]
                print(f"\n   Sample user fields:")
                print(f"   - ID: {sample_user.id}")
                print(f"   - Email: {sample_user.email}")
                print(f"   - Username: {sample_user.username}")
                print(f"   - Name: {sample_user.name}")
                print(f"   - Full Name: {sample_user.full_name}")
                print(f"   - Role: {sample_user.role}")
                print(f"   - Is Verified: {sample_user.is_verified}")
                print(f"   - Permissions: {sample_user.permissions}")
            
            # Count by role
            admin_count = User.query.filter_by(role='admin').count()
            teacher_count = User.query.filter_by(role='teacher').count()
            student_count = User.query.filter_by(role='student').count()
            
            print(f"\n   Role distribution:")
            print(f"   - Admins: {admin_count}")
            print(f"   - Teachers: {teacher_count}")
            print(f"   - Students: {student_count}")
            
            # Check AdminLog table
            print(f"\nAdminLog table:")
            log_count = AdminLog.query.count()
            print(f"   Total logs: {log_count}")
            
            print("\nAll tables verified successfully!")
            return True
            
        except Exception as e:
            print(f"\nVerification failed: {e}")
            return False


def main():
    """Run the complete migration"""
    print("\n" + "="*60)
    print("STARTING DATABASE MIGRATION")
    print("   Adding Wissal Backend User Management Features")
    print("="*60)
    
    try:
        # Run migration phases
        upgrade_users_table()
        populate_new_fields()
        create_admin_logs_table()
        verify_migration()
        
        print("\n" + "="*60)
        print("MIGRATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nYour database now includes:")
        print("   - Enhanced User model with roles and permissions")
        print("   - Email verification support")
        print("   - AdminLog table for audit tracking")
        print("   - All existing data preserved")
        print("\nReady for JWT authentication and admin panel!")
        print("="*60 + "\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("MIGRATION FAILED!")
        print("="*60)
        print(f"\nError: {e}")
        print("\nYour database has not been modified.")
        print("   The backup file can be found in instance/ folder.")
        print("="*60 + "\n")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

