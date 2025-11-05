"""
Management CLI for Project Management System
Run: python manage.py <command>
"""
import sys
import getpass
import re
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password

# Import all models to ensure relationships are properly initialized
from app.models.user import User
from app.models.project import Project
from app.models.task import Task


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 100:
        return False, "Password must not exceed 100 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
    
    return True, ""


def create_admin():
    """Create an admin user interactively"""
    print("\n" + "="*60)
    print("CREATE ADMIN USER")
    print("="*60 + "\n")
    
    db: Session = SessionLocal()
    
    try:
        # Get email
        while True:
            email = input("Admin email: ").strip()
            if not email:
                print("❌ Email cannot be empty\n")
                continue
            
            if not validate_email(email):
                print("❌ Invalid email format\n")
                continue
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                print(f"❌ Error: User with email '{email}' already exists")
                print(f"   Role: {existing_user.role}")
                print(f"   Name: {existing_user.full_name}\n")
                
                choice = input("Try another email? (y/n): ").strip().lower()
                if choice != 'y':
                    print("\n❌ Admin creation cancelled.\n")
                    return
                continue
            
            break
        
        # Get full name
        while True:
            full_name = input("Full name: ").strip()
            if not full_name:
                print("❌ Full name cannot be empty\n")
                continue
            
            if len(full_name) < 3:
                print("❌ Full name must be at least 3 characters\n")
                continue
            
            if len(full_name) > 100:
                print("❌ Full name must not exceed 100 characters\n")
                continue
            
            break
        
        # Get password
        while True:
            password = getpass.getpass("Password: ")
            if not password:
                print("❌ Password cannot be empty\n")
                continue
            
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"❌ {error_msg}\n")
                continue
            
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                print("❌ Passwords don't match. Please try again.\n")
                continue
            
            break
        
        # Create admin user
        print("\n⏳ Creating admin user...")
        
        admin_user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
            disabled=False
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("\n" + "="*60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"ID:         {admin_user.id}")
        print(f"Email:      {admin_user.email}")
        print(f"Name:       {admin_user.full_name}")
        print(f"Role:       {admin_user.role}")
        print(f"Created:    {admin_user.created_at}")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Admin creation cancelled by user.\n")
        db.rollback()
    except Exception as e:
        print(f"\n❌ Error creating admin user: {str(e)}\n")
        db.rollback()
    finally:
        db.close()


def list_users():
    """List all users in the database"""
    print("\n" + "="*80)
    print("ALL USERS")
    print("="*80 + "\n")
    
    db: Session = SessionLocal()
    
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        
        if not users:
            print("No users found in the database.\n")
            return
        
        print(f"{'ID':<5} {'Email':<35} {'Name':<25} {'Role':<10} {'Active':<8}")
        print("-"*80)
        
        for user in users:
            status = "Yes" if user.is_active else "No"
            print(f"{user.id:<5} {user.email:<35} {user.full_name:<25} {user.role:<10} {status:<8}")
        
        print("-"*80)
        print(f"Total users: {len(users)}\n")
        
    except Exception as e:
        print(f"❌ Error listing users: {str(e)}\n")
    finally:
        db.close()


def change_user_role():
    """Change a user's role between 'user' and 'admin'"""
    print("\n" + "="*60)
    print("CHANGE USER ROLE")
    print("="*60 + "\n")
    
    db: Session = SessionLocal()
    
    try:
        # Get user email or ID
        identifier = input("Enter user email or ID: ").strip()
        
        if not identifier:
            print("❌ Email or ID cannot be empty\n")
            return
        
        # Try to find user by ID first, then by email
        user = None
        if identifier.isdigit():
            user = db.query(User).filter(User.id == int(identifier)).first()
        else:
            user = db.query(User).filter(User.email == identifier).first()
        
        if not user:
            print(f"❌ User not found: {identifier}\n")
            return
        
        # Display current user info
        print(f"\n📋 Current User Info:")
        print(f"   ID:    {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Name:  {user.full_name}")
        print(f"   Role:  {user.role}")
        print()
        
        # Ask for new role
        print("Available roles: admin, user")
        new_role = input(f"Enter new role (current: {user.role}): ").strip().lower()
        
        if new_role not in ['admin', 'user']:
            print("❌ Invalid role. Must be 'admin' or 'user'\n")
            return
        
        if new_role == user.role:
            print(f"⚠️  User already has role '{new_role}'\n")
            return
        
        # Confirm change
        confirm = input(f"\nChange role from '{user.role}' to '{new_role}'? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Role change cancelled.\n")
            return
        
        # Update role
        user.role = new_role
        db.commit()
        
        print(f"\n✅ User role updated successfully!")
        print(f"   {user.email} is now an '{new_role}'\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.\n")
        db.rollback()
    except Exception as e:
        print(f"\n❌ Error changing user role: {str(e)}\n")
        db.rollback()
    finally:
        db.close()


def show_help():
    """Display help information"""
    print("\n" + "="*60)
    print("PROJECT MANAGEMENT SYSTEM - CLI MANAGEMENT TOOL")
    print("="*60 + "\n")
    
    print("Available commands:\n")
    print("  create-admin     Create a new admin user interactively")
    print("  list-users       List all users in the database")
    print("  change-role      Change a user's role (admin/user)")
    print("  help             Show this help message")
    print("\nUsage:")
    print("  python manage.py <command>\n")
    print("Examples:")
    print("  python manage.py create-admin")
    print("  python manage.py list-users")
    print("  python manage.py change-role\n")


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'create-admin': create_admin,
        'list-users': list_users,
        'change-role': change_user_role,
        'help': show_help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"\n❌ Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()

