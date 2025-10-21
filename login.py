class LoginManager:
    def __init__(self, students):
        self.students = students  # List of Student objects

    def login(self):
        student_id = input("Enter your Student ID to login: ").strip()

        # Ensure only digits are entered
        if not student_id.isdigit():
            print("❌ Invalid input: only numeric IDs are allowed.")
            return False

        # Check if student exists
        for student in self.students:
            if student.student_id == student_id:
                print(f"✅ Welcome, {student.first_name} {student.last_name}!")
                return True

        print("❌ Student ID not found in the system.")
        return False