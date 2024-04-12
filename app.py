from datetime import datetime, timedelta
import jwt
import bcrypt
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['users']
collection = db['users']

# Secret key for JWT token
SECRET_KEY = "your_secret_key"

def generate_jwt_token(username: str) -> str:
    # Set the expiration time for the token (e.g., 24 hours from now)
    expiration_time = datetime.utcnow() + timedelta(hours=24)
    
    # Define the payload of the token
    payload = {"username": username, "exp": expiration_time}
    
    # Generate the token using the payload and secret key
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return token

def signup():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if username already exists
    if collection.find_one({"username": username}):
        print("Username already exists. Please choose another username.")
        return

    # Generate JWT token for the user
    token = generate_jwt_token(username)

    # Insert the user and token into the database
    user = {"username": username, "password": hashed_password, "token": token}
    collection.insert_one(user)
    print("Signup successful.")
    

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Retrieve the user from the database
    user = collection.find_one({"username": username})

    # Check if the user exists and if the password is correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        print("Login successful.")
    else:
        print("Invalid username or password.")

def main():
    while True:
        print("\n1. Signup\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            signup()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()