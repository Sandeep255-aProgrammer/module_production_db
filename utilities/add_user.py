import datetime
from werkzeug.security import generate_password_hash
from main import app, db, User  # Import `app`, `db`, and `User` from `main.py`

def add_user(username, plain_password, name):
    # Generate a hashed password
    hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256', salt_length=8)
    
    # Create a new User instance
    new_user = User(
        username=username,
        password=hashed_password,
        name=name,
        created_at=datetime.datetime.utcnow(),  # Use the current datetime
        is_active=True  # Set as active by default
    )
    
    # Add and commit the new user to the database within an application context
    with app.app_context():  # Add this line to establish an application context
        with db.session.begin():
            db.session.add(new_user)
            db.session.commit()
    print(f"User '{username}' added successfully.")

# Get user details from terminal input
if __name__ == "__main__":
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    name = input("Enter the name: ")
    
    add_user(username, password, name)

