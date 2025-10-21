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
        total = sum(int(d) for d in digits_str)
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