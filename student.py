import csv
from serial import SerialNumberGenerator

class Student:
    def __init__(self, first_name, last_name, major_code, major_name, start_year, serial_number, student_id):
        self.first_name = first_name
        self.last_name = last_name
        self.major_code = major_code
        self.major_name = major_name
        self.start_year = start_year
        self.serial_number = serial_number
        self.student_id = student_id

    def to_dict(self):
        return {
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Major": self.major_name,
            "Start Year": self.start_year,
            "Student ID": self.student_id
        }

class StudentManager:
    def __init__(self):
        self.majors = {
            1: "Cyber Security",
            2: "Software Engineering",
            3: "Digital Industrial Engineering",
            4: "Data Science and AI"
        }
        self.students = []
        self.serial_counter = 1  # Start from 0001

    def add_student(self, first_name, last_name, major_code, year):
        if major_code not in self.majors:
            print("❌ Invalid major code.")
            return

        serial_str = SerialNumberGenerator.generate_serial()
        major_str = str(major_code)
        base_id = major_str + year + serial_str
        checksum_digit = self.calculate_checksum(base_id)
        full_id = base_id + str(checksum_digit)

        student = Student(
            first_name,
            last_name,
            major_code,
            self.majors[major_code],
            year,
            serial_str,
            full_id
        )

        self.students.append(student)
        print(f"✅ Student added. ID: {full_id}")

    def calculate_checksum(self, digits_str):
        """
        Calculate Luhn checksum for the given base ID string (without the check digit).
        Doubling starts from the rightmost digit's neighbor (the second-to-last digit overall).
        """
        digits = [int(d) for d in digits_str]
        total = 0
        reverse_digits = digits[::-1]

        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:  # <-- shift parity to match official Luhn standard
                doubled = d * 2
                if doubled > 9:
                    doubled -= 9
                total += doubled
            else:
                total += d

        return (10 - (total % 10)) % 10

    def list_students(self):
        if not self.students:
            print("No students added yet.")
            return

        print("\n📋 Registered Students:")
        for s in self.students:
            print(f"{s.student_id} - {s.first_name} {s.last_name} ({s.major_name}, {s.start_year})")

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["First Name", "Last Name", "Major", "Start Year", "Student ID"])
            writer.writeheader()
            for student in self.students:
                writer.writerow(student.to_dict())

        print(f"💾 Students saved to {filename}")

    def load_from_csv(self, filename):
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Detect major code from major name
                    major_code = None
                    for code, name in self.majors.items():
                        if name == row["Major"]:
                            major_code = code
                            break

                    if major_code is None:
                        print(f"⚠️ Unknown major in CSV: {row['Major']}")
                        continue

                    student_id = row["Student ID"]
                    serial_number = student_id[5:9] if len(student_id) >= 10 else ""

                    student = Student(
                        first_name=row["First Name"],
                        last_name=row["Last Name"],
                        major_code=major_code,
                        major_name=row["Major"],
                        start_year=row["Start Year"],
                        serial_number=serial_number,
                        student_id=student_id
                    )

                    self.students.append(student)

            print(f"✅ Loaded {len(self.students)} students from {filename}")
        except FileNotFoundError:
            print(f"⚠️ File {filename} not found. Starting with empty student list.")

    def validate_id(self, student_id):
        digits = [int(d) for d in student_id]
        check_digit = digits[-1]
        digits = digits[:-1]

        calculated_checksum = self.calculate_checksum("".join(map(str, digits)))
        return check_digit == calculated_checksum