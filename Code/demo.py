import sqlite3
import hashlib
import os

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(f"Error: {e}")
    return None

def create_table(conn):
    """Create a table for storing user credentials."""
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, salt BLOB NOT NULL, password TEXT NOT NULL)''')
    except Exception as e:
        print(f"Error: {e}")

def hash_password(password):
    """Hash a password for storing."""
    salt = os.urandom(32)  # A new salt for each user
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, hashed_password

def store_credentials(conn, username, password):
    """Store a new user's credentials in the database."""
    salt, hashed_password = hash_password(password)
    try:
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, salt, hashed_password))
        conn.commit()
        print("Account created successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Choose a different username.")
    except Exception as e:
        print(f"Error: {e}")

def verify_credentials(conn, username, password):
    """Verify a user's login credentials."""
    c = conn.cursor()
    c.execute("SELECT salt, password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        salt, stored_password = result
        hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
        return stored_password == hashed_password
    return False

def run_demo():
    database = "pythonsqlite.db"
    conn = create_connection(database)

    if conn is not None:
        create_table(conn)

        while True:
            print("\nMain Menu:")
            print("1. Create new account")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                store_credentials(conn, username, password)
            elif choice == "2":
                while True:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    if verify_credentials(conn, username, password):
                        print("Successfully Logged In!")
                        break
                    else:
                        print("Invalid credentials. Try again or close program.")
                        try_again = input("Try again? (yes/no): ").lower()
                        if try_again == "no":
                            break
                        elif try_again == "yes":
                            print("Please try again!")
                            continue
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")
            elif choice == "3":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    run_demo()
