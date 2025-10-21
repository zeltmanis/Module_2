class LoginManager:
    def __init__(self, students):
        self.students = students  # List of Student objects

    def login(self):
        student_id = input("Enter your Student ID to login: ").strip()
        # Search for student with this ID
        for student in self.students:
            if student.student_id == student_id:
                print(f"✅ Welcome, {student.first_name} {student.last_name}!")
                return True

        print("❌ Invalid Student ID. Please try again.")
        return False