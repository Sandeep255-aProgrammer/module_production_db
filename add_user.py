from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import Flask
from database_table1 import db, UserTable  # Adjust the import to where your UserTable model is defined

# Sample user data dictionary to add a new user to the UserTable
user_data = {
    "username": "newuser123",
    "password": "securepassword123",  # Make sure to hash passwords before saving to the database
    "name": "John Doe",
    "created_at": datetime.utcnow(),  # Timestamp for created_at
    "is_active": True  # By default, user is active
}

# Initialize Flask app and configure database URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///niser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db.init_app(app)

# Ensure all tables are created
with app.app_context():
    db.create_all()

# Function to add the user
def add_user_to_db(user_data):
    try:
        # Attempt to add the user using the class method `add_user`
        with app.app_context():
            user = UserTable.add_user(user_data)  # Calls the add_user method on UserTable
        print(f"User {user.username} added successfully!")
    except IntegrityError as e:
        print(f"Integrity error: {str(e)} - This could be a duplicate username or some constraint violation.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# Call the function to add the user
add_user_to_db(user_data)

