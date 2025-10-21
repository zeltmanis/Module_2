class LoginManager:
    def __init__(self, students):
        self.students = students  # List of Student objects

    def login(self):
        student_id = input("Enter your Student ID to login: ").strip()

        # Validate Luhn checksum before checking student list
        from student import StudentManager  # import here to avoid circular import
        temp_manager = StudentManager()
        if not temp_manager.validate_id(student_id):
            print("❌ Invalid Student ID (checksum failed). Possible typing error.")
            return False

        for student in self.students:
            if student.student_id == student_id:
                print(f"✅ Welcome, {student.first_name} {student.last_name}!")
                return True

        print("❌ Student ID not found in the system.")
        return False