from student import StudentManager
from login import LoginManager
from error_detection_test import generate_error_report

def main():
    manager = StudentManager()
    manager.load_from_csv("students.csv")
    login_manager = LoginManager(manager.students)

    while True:
        print("\n🎓 Student ID System")
        print("1. Add new student")
        print("2. List all students")
        print("3. Save to CSV")
        print("4. Login")
        print("5. Run Error Detection Test")
        print("6. Exit")


        choice = input("Choose an option (1-6): ")

        if choice == '1':
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            print("Majors:")
            for code, name in manager.majors.items():
                print(f"{code}: {name}")
            major_code = int(input("Enter major code (1-4): "))
            year = input("Start year (e.g., 2025): ").strip()

            manager.add_student(first_name, last_name, major_code, year)

        elif choice == '2':
            manager.list_students()

        elif choice == '3':
            manager.save_to_csv("students.csv")

        elif choice == '4':
            login_manager.login()

        elif choice == '5':
            print("\n🧪 Running Error Detection Test...")
            generate_error_report(input_file="students.csv")
            print("✅ Test finished. Check 'error_detection_results.csv' for details.")

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()