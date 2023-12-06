import demo
import view

def show_menu():
    print("\nMain Menu:")
    print("1. Play Demo")
    print("2. View SQL Data")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice

def main():
    while True:
        choice = show_menu()

        if choice == '1':
            demo.run_demo()
        elif choice == '2':
            view.run_view()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
