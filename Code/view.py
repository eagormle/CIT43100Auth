import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

def query_all_users(conn):
    """Query all users in the users table."""
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM users")

        rows = c.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(e)

def purge_all_data(conn):
    """Delete all data from the users table."""
    try:
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()
        print("All data purged successfully.")
    except Exception as e:
        print(e)

def show_menu():
    """Display the menu options."""
    print("\nMenu:")
    print("1. View all data")
    print("2. Purge all data")
    print("3. Quit")
    choice = input("Enter your choice: ")
    return choice

def run_view():
    database = "pythonsqlite.db"
    conn = create_connection(database)

    if conn is not None:
        while True:
            choice = show_menu()

            if choice == '1':
                query_all_users(conn)
            elif choice == '2':
                confirm = input("Are you sure you want to purge all data? (yes/no): ")
                if confirm.lower() == 'yes':
                    purge_all_data(conn)
            elif choice == '3':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    run_view()
