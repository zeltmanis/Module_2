import csv
import random
import string
from student import StudentManager

# ----- Error generators -----
def one_digit_typo(student_id):
    """Change one random digit (except the check digit) to a different digit."""
    idx = random.randint(0, len(student_id) - 2)
    orig = student_id[idx]
    choices = [str(d) for d in range(10) if str(d) != orig]
    new_digit = random.choice(choices)
    return student_id[:idx] + new_digit + student_id[idx + 1:]

def alphabet_substitution(student_id):
    """Replace one digit (except the check digit) with a random lowercase letter."""
    idx = random.randint(0, len(student_id) - 2)
    letter = random.choice(string.ascii_lowercase)
    return student_id[:idx] + letter + student_id[idx + 1:]

def adjacent_swap(student_id):
    """
    Swap two adjacent digits somewhere in the base part.
    If the chosen position would touch the check digit, pick another.
    """
    if len(student_id) < 3:
        return student_id  # can't swap
    idx = random.randint(0, len(student_id) - 3)  # ensure swap is not touching final check digit
    s = list(student_id)
    s[idx], s[idx + 1] = s[idx + 1], s[idx]
    return "".join(s)

def repeated_digit(student_id):
    """
    Replace a digit with the same as one of its neighbors (left or right),
    simulating an accidental duplication choice while keeping length constant.
    """
    if len(student_id) < 3:
        return student_id
    idx = random.randint(0, len(student_id) - 2)  # avoid check digit
    # choose neighbor index (left or right within base part)
    neighbors = []
    if idx - 1 >= 0:
        neighbors.append(idx - 1)
    if idx + 1 <= len(student_id) - 2:  # ensure not the check digit
        neighbors.append(idx + 1)
    if not neighbors:
        return student_id
    n_idx = random.choice(neighbors)
    new_digit = student_id[n_idx]
    return student_id[:idx] + new_digit + student_id[idx + 1:]

# Map error type names to functions
ERROR_TYPES = {
    "1-digit-typo": one_digit_typo,
    "alphabet-substitution": alphabet_substitution,
    "adjacent-swap": adjacent_swap,
    "repeated-digit": repeated_digit
}

def generate_error_report(
    input_file="students.csv",
    output_file="error_detection_results.csv",
    tests_per_student=20
):
    """
    Generate errors of different types for each student and write results to CSV.
    tests_per_student is the number of simulated erroneous IDs per student (plus the original ID row).
    """
    sm = StudentManager()
    sm.load_from_csv(input_file)

    results = []
    total_tests = 0
    detected_errors = 0

    for student in sm.students:
        # Add the correct ID row
        results.append({
            "Student Name": f"{student.first_name} {student.last_name}",
            "Original ID": student.student_id,
            "Tested ID": student.student_id,
            "Error Type": "original",
            "Is Valid": "✅ True" if sm.validate_id(student.student_id) else "❌ False",
            "Note": "original"
        })

        # Create erroneous IDs
        for _ in range(tests_per_student):
            err_type = random.choice(list(ERROR_TYPES.keys()))
            wrong_id = ERROR_TYPES[err_type](student.student_id)

            # Validate but guard against exceptions for non-digit strings
            try:
                is_valid = sm.validate_id(wrong_id)
            except Exception:
                # If validate_id wasn't defensive, treat non-digit as invalid
                is_valid = False

            note = ""
            if not wrong_id.isdigit():
                note = "non-digit present"
            total_tests += 1
            if not is_valid:
                detected_errors += 1

            results.append({
                "Student Name": f"{student.first_name} {student.last_name}",
                "Original ID": student.student_id,
                "Tested ID": wrong_id,
                "Error Type": err_type,
                "Is Valid": "✅ True" if is_valid else "❌ False",
                "Note": note
            })

    # Save CSV
    fieldnames = ["Student Name", "Original ID", "Tested ID", "Error Type", "Is Valid", "Note"]
    with open(output_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    success_rate = detected_errors / total_tests * 100 if total_tests else 0.0
    print(f"✅ Error detection success rate: {success_rate:.2f}% ({detected_errors}/{total_tests} errors caught)")
    print(f"💾 Results saved to {output_file}")

    try:
        from tabulate import tabulate  # pip install tabulate if missing

        # Show only the first 30 rows for readability
        sample_rows = results[:30]
        print("\n📊 Sample Error Detection Results (first 30 rows):")
        print(tabulate(sample_rows, headers="keys", tablefmt="grid"))
    except ImportError:
        print("⚠️ Install 'tabulate' to see pretty tables: pip install tabulate")

    # --- NEW: generate not-caught-invalid report ---
    not_caught = [r for r in results if r["Is Valid"] == "✅ True" and r["Error Type"] != "original"]

    if not_caught:
        not_caught_file = output_file.replace(".csv", "_not_caught.csv")
        with open(not_caught_file, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(not_caught)

        print(f"⚠️ {len(not_caught)} invalid IDs were NOT detected. See {not_caught_file} for details.")

        # Optional: pretty print first 20 in console
        try:
            from tabulate import tabulate
            print("\n📌 Sample of NOT detected invalid IDs:")
            print(tabulate(not_caught[:20], headers="keys", tablefmt="grid"))
        except ImportError:
            pass
    else:
        print("✅ All invalid IDs were successfully detected!")

if __name__ == "__main__":
    generate_error_report()