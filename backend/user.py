import bcrypt
from backend.query import execute_query

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def email_exist(email):
    """Check if an email exists in the User table."""
    return execute_query("SELECT 1 FROM User WHERE email = ?", (email,), fetchone=True) is not None

def verify_password(stored_hash, password):
    """Verify if the provided password matches the stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def get_old_password(user_id: int) -> str:
    """Fetch the old password from the database for a given user."""
    result = execute_query("SELECT password FROM User WHERE id = ?", (user_id,), fetchone=True)
    return result[0] if result else None

def update_user_info(user_id: int, **kwargs):
    """Update user information dynamically."""
    if not kwargs:
        raise ValueError("No fields provided for update.")

    columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
    values = list(kwargs.values()) + [user_id]
    query = f"UPDATE User SET {columns} WHERE id = ?"

    execute_query(query, values, commit=True)

def get_user_type_by_email(email):
    """Retrieve the user type for a given email."""
    result = execute_query("SELECT user_type FROM User WHERE email = ?", (email,), fetchone=True)
    return result[0] if result else "User not found"

def get_first_name_by_email(email):
    """Retrieve the first name from other_names for a given email."""
    result = execute_query("SELECT other_names FROM User WHERE email = ?", (email,), fetchone=True)
    return result[0].split()[0] if result else "User"

def create_user(email, password, last_name, other_names, user_type, matric_number=None, title=None):
    """Insert a new user into the database."""
    password_hash = hash_password(password)
    query = '''
    INSERT INTO User (email, password, last_name, other_names, user_type, matric_number, title)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    execute_query(query, (email, password_hash, last_name, other_names, user_type, matric_number, title), commit=True)
    return True

def authenticate_user(email, password):
    """Authenticate a user by checking email and password."""
    result = execute_query("SELECT password FROM User WHERE email = ?", (email,), fetchone=True)

    if result is None:
        raise ValueError(f"Authentication failed: No user found with email {email}")

    stored_hash = result[0]
    if not verify_password(stored_hash, password):
        raise ValueError("Authentication failed: Incorrect password")

    return True

def get_user_type_by_id(user_id):
    """Fetches the user type from the database using execute_query."""
    query = "SELECT user_type FROM User WHERE id = ?"
    result = execute_query(query, (user_id,), fetchone=True)
    return result[0] if result else None

def get_user_profile_by_email(email):
    """Fetches a user's profile by email."""
    name = get_first_name_by_email(email)

    query = """
        SELECT id, last_name, other_names, user_type, matric_number, title 
        FROM user 
        WHERE email = ?
    """
    user = execute_query(query, (email,), fetchone=True)
    return user