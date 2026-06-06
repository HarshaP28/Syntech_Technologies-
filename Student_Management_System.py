# ================================================================
#   STUDENT MANAGEMENT SYSTEM
#   Language : Python 3
#   Storage  : JSON file  (students.json — auto-created)
#   Features : Add | View | Search | Update | Delete | Export CSV
#   Run      : python student_management.py
# ================================================================

import json
import csv
import os
import datetime

# ──────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────

JSON_FILE = "students.json"        # where all records are saved
SEPARATOR = "=" * 60

# ──────────────────────────────────────────────
#  FILE / STORAGE HELPERS
# ──────────────────────────────────────────────

def load_students():
    """
    Load all student records from the JSON file.
    Returns an empty list if the file doesn't exist yet.
    """
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r") as f:
        return json.load(f)


def save_students(students):
    """
    Save the full list of student records back to the JSON file.
    indent=4 makes the file human-readable.
    """
    with open(JSON_FILE, "w") as f:
        json.dump(students, f, indent=4)


def next_id(students):
    """
    Auto-generate the next student ID.
    Finds the current maximum ID and adds 1.
    Starts at S001 if there are no records yet.
    """
    if not students:
        return "S001"
    # Extract numeric part of IDs like "S001" → 1
    nums = [int(s["id"][1:]) for s in students]
    return f"S{max(nums) + 1:03d}"

# ──────────────────────────────────────────────
#  INPUT VALIDATION HELPERS
# ──────────────────────────────────────────────

def get_non_empty(prompt):
    """Keep asking until the user types something non-blank."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  ⚠  This field cannot be empty. Please try again.")


def get_float_in_range(prompt, min_val, max_val):
    """
    Keep asking until the user enters a decimal number
    within [min_val, max_val].
    """
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  ⚠  Enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Please enter a valid number.")


def get_int_in_range(prompt, min_val, max_val):
    """Keep asking until the user enters an integer within range."""
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  ⚠  Enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Please enter a whole number.")


def grade_from_marks(marks):
    """
    Convert a numeric mark (0–100) into a letter grade.
    """
    if marks >= 90: return "A+"
    if marks >= 80: return "A"
    if marks >= 70: return "B"
    if marks >= 60: return "C"
    if marks >= 50: return "D"
    return "F"

# ──────────────────────────────────────────────
#  DISPLAY HELPERS
# ──────────────────────────────────────────────

def print_header(title):
    print("\n" + SEPARATOR)
    print(f"  {title}")
    print(SEPARATOR)


def print_student_card(s):
    """Pretty-print a single student record."""
    print(f"""
  ┌─────────────────────────────────────┐
  │  ID       : {s['id']:<26}│
  │  Name     : {s['name']:<26}│
  │  Age      : {s['age']:<26}│
  │  Course   : {s['course']:<26}│
  │  Marks    : {s['marks']:<26}│
  │  Grade    : {s['grade']:<26}│
  │  Email    : {s['email']:<26}│
  │  Added on : {s['date']:<26}│
  └─────────────────────────────────────┘""")


def print_table(students):
    """Print all students in a compact table format."""
    if not students:
        print("\n  No records found.")
        return

    print(f"\n  {'ID':<6} {'Name':<20} {'Age':<5} {'Course':<18} {'Marks':<7} {'Grade':<6} {'Email'}")
    print("  " + "-" * 80)
    for s in students:
        print(f"  {s['id']:<6} {s['name']:<20} {s['age']:<5} {s['course']:<18} {s['marks']:<7} {s['grade']:<6} {s['email']}")
    print(f"\n  Total records: {len(students)}")

# ──────────────────────────────────────────────
#  CORE OPERATIONS  (CRUD)
# ──────────────────────────────────────────────

# ── CREATE ────────────────────────────────────

def add_student():
    """Collect details from the user and save a new student record."""
    print_header("ADD NEW STUDENT")

    students = load_students()
    student_id = next_id(students)
    print(f"  Auto-assigned ID: {student_id}\n")

    name   = get_non_empty("  Full Name     : ")
    age    = get_int_in_range("  Age (5–100)   : ", 5, 100)
    course = get_non_empty("  Course/Class  : ")
    marks  = get_float_in_range("  Marks (0–100) : ", 0, 100)
    email  = get_non_empty("  Email Address : ")

    grade = grade_from_marks(marks)
    date  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    new_student = {
        "id"    : student_id,
        "name"  : name,
        "age"   : age,
        "course": course,
        "marks" : marks,
        "grade" : grade,
        "email" : email,
        "date"  : date
    }

    students.append(new_student)
    save_students(students)

    print(f"\n  ✅  Student '{name}' added successfully with ID {student_id}!")
    print_student_card(new_student)


# ── READ (View All) ───────────────────────────

def view_all_students():
    """Display every student in a table."""
    print_header("ALL STUDENTS")
    students = load_students()
    if not students:
        print("\n  No students found. Add some records first.")
        return
    print_table(students)


# ── READ (Search) ─────────────────────────────

def search_student():
    """
    Search by ID, name (partial match), or course.
    Case-insensitive.
    """
    print_header("SEARCH STUDENT")
    print("  Search by:  1) ID    2) Name    3) Course")
    choice = get_int_in_range("  Your choice: ", 1, 3)

    students = load_students()
    results  = []

    if choice == 1:
        sid = get_non_empty("  Enter Student ID: ").upper()
        results = [s for s in students if s["id"] == sid]

    elif choice == 2:
        keyword = get_non_empty("  Enter name (or part of it): ").lower()
        results = [s for s in students if keyword in s["name"].lower()]

    elif choice == 3:
        course = get_non_empty("  Enter course name: ").lower()
        results = [s for s in students if course in s["course"].lower()]

    if results:
        print(f"\n  Found {len(results)} matching record(s):")
        print_table(results)
    else:
        print("\n  ❌  No matching students found.")


# ── UPDATE ────────────────────────────────────

def update_student():
    """
    Let the user update any individual field of a student record.
    Pressing Enter without typing keeps the existing value.
    """
    print_header("UPDATE STUDENT RECORD")

    students = load_students()
    if not students:
        print("\n  No records to update.")
        return

    sid = get_non_empty("  Enter Student ID to update: ").upper()
    student = next((s for s in students if s["id"] == sid), None)

    if not student:
        print(f"\n  ❌  Student with ID '{sid}' not found.")
        return

    print("\n  Current record:")
    print_student_card(student)
    print("\n  Press ENTER to keep the current value for any field.\n")

    # For each field, show current value and allow override
    new_name = input(f"  Name     [{student['name']}]: ").strip()
    if new_name:
        student["name"] = new_name

    new_age = input(f"  Age      [{student['age']}]: ").strip()
    if new_age:
        try:
            val = int(new_age)
            if 5 <= val <= 100:
                student["age"] = val
            else:
                print("  ⚠  Age out of range — kept original.")
        except ValueError:
            print("  ⚠  Invalid number — kept original.")

    new_course = input(f"  Course   [{student['course']}]: ").strip()
    if new_course:
        student["course"] = new_course

    new_marks = input(f"  Marks    [{student['marks']}]: ").strip()
    if new_marks:
        try:
            val = float(new_marks)
            if 0 <= val <= 100:
                student["marks"] = val
                student["grade"] = grade_from_marks(val)   # recalculate grade
            else:
                print("  ⚠  Marks out of range — kept original.")
        except ValueError:
            print("  ⚠  Invalid number — kept original.")

    new_email = input(f"  Email    [{student['email']}]: ").strip()
    if new_email:
        student["email"] = new_email

    save_students(students)
    print(f"\n  ✅  Record for '{student['name']}' updated successfully!")
    print_student_card(student)


# ── DELETE ────────────────────────────────────

def delete_student():
    """Delete a student record after confirmation."""
    print_header("DELETE STUDENT")

    students = load_students()
    if not students:
        print("\n  No records to delete.")
        return

    sid = get_non_empty("  Enter Student ID to delete: ").upper()
    student = next((s for s in students if s["id"] == sid), None)

    if not student:
        print(f"\n  ❌  Student with ID '{sid}' not found.")
        return

    print_student_card(student)
    confirm = input(f"\n  Are you sure you want to delete '{student['name']}'? (yes/no): ").strip().lower()

    if confirm == "yes":
        students = [s for s in students if s["id"] != sid]
        save_students(students)
        print(f"\n  ✅  Student '{student['name']}' (ID: {sid}) deleted successfully.")
    else:
        print("\n  ↩  Deletion cancelled.")


# ── EXPORT TO CSV ─────────────────────────────

def export_to_csv():
    """
    Export all student records to a CSV file.
    Useful for opening in Excel or Google Sheets.
    """
    print_header("EXPORT TO CSV")

    students = load_students()
    if not students:
        print("\n  No records to export.")
        return

    filename = f"students_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fields   = ["id", "name", "age", "course", "marks", "grade", "email", "date"]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(students)

    print(f"\n  ✅  {len(students)} record(s) exported to '{filename}' successfully!")


# ── STATISTICS ────────────────────────────────

def show_statistics():
    """Show quick summary stats about all students."""
    print_header("STUDENT STATISTICS")

    students = load_students()
    if not students:
        print("\n  No records available.")
        return

    marks_list = [s["marks"] for s in students]
    avg   = sum(marks_list) / len(marks_list)
    high  = max(marks_list)
    low   = min(marks_list)

    top    = [s for s in students if s["marks"] == high]
    bottom = [s for s in students if s["marks"] == low]

    grade_counts = {}
    for s in students:
        grade_counts[s["grade"]] = grade_counts.get(s["grade"], 0) + 1

    course_counts = {}
    for s in students:
        course_counts[s["course"]] = course_counts.get(s["course"], 0) + 1

    print(f"""
  Total Students   : {len(students)}
  Average Marks    : {avg:.2f}
  Highest Marks    : {high}  → {', '.join(s['name'] for s in top)}
  Lowest Marks     : {low}   → {', '.join(s['name'] for s in bottom)}

  Grade Distribution:""")
    for g in sorted(grade_counts):
        bar = "█" * grade_counts[g]
        print(f"    {g:<4}: {bar}  ({grade_counts[g]})")

    print("\n  Students per Course:")
    for c, count in sorted(course_counts.items()):
        print(f"    {c:<20}: {count}")

# ──────────────────────────────────────────────
#  MAIN MENU
# ──────────────────────────────────────────────

def main_menu():
    menu = """
  ┌─────────────────────────────────┐
  │   STUDENT MANAGEMENT SYSTEM     │
  ├─────────────────────────────────┤
  │  1. Add Student                 │
  │  2. View All Students           │
  │  3. Search Student              │
  │  4. Update Student              │
  │  5. Delete Student              │
  │  6. Export to CSV               │
  │  7. Statistics                  │
  │  8. Exit                        │
  └─────────────────────────────────┘"""

    actions = {
        "1": add_student,
        "2": view_all_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": export_to_csv,
        "7": show_statistics,
    }

    while True:
        print(menu)
        choice = input("  Enter your choice (1–8): ").strip()

        if choice == "8":
            print("\n  👋  Goodbye! Data saved to students.json\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  ⚠  Invalid choice. Please enter a number from 1 to 8.")

# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    main_menu()