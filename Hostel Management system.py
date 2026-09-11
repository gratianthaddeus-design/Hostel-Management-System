import json
import os

DATA_FILE = "hostel_data.json"


# ============================================================
# (a) DATA SETUP
# ============================================================

def create_hostel_data():
    """Create the predefined hostel blocks, rooms and capacities."""

    hostel_blocks = {                                                       #A nested dictionary is used so as to group related information under 
                                                                                    #under one key
        "Block 100": {
            "rooms": {
                "100-A": {"capacity": 6, "occupants": []},
                "100-B": {"capacity": 5, "occupants": []},
                "100-C": {"capacity": 3, "occupants": []}
            }
        },

        "Block 200": {
            "rooms": {
                "200-A": {"capacity": 6, "occupants": []},
                "200-B": {"capacity": 5, "occupants": []},
                "200-C": {"capacity": 3, "occupants": []}
            }
        },

        "Block 300": {
            "rooms": {
                "300-A": {"capacity": 6, "occupants": []},
                "300-B": {"capacity": 5, "occupants": []},
                "300-C": {"capacity": 3, "occupants": []}
            }
        }
    }

    students = {}

    return {
        "hostel_blocks": hostel_blocks,
        "students": students
    }

# ============================================================
# INPUT VALIDATION
# ============================================================

def get_positive_float(prompt):
    """Get a positive decimal number."""

    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Please enter an amount greater than 0.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_non_negative_float(prompt):
    """Get zero or a positive decimal number."""

    while True:
        try:
            value = float(input(prompt))

            if value < 0:
                print("Please enter 0 or a positive amount.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a number.")



# Global data (lets a function change the one shared copy of a variable)            
hostel_blocks = {}
students = {}



# ============================================================
#  OCCUPANCY OVERVIEW
# ============================================================

def print_occupancy_overview():
    """Print a brief occupancy overview for all hostel blocks."""

    print("\n" + "=" * 60)
    print("HOSTEL OCCUPANCY OVERVIEW")
    print("=" * 60)

    for block_name, block in hostel_blocks.items():

        total_capacity = 0
        total_occupied = 0

        for room in block["rooms"].values():
            total_capacity += room["capacity"]
            total_occupied += len(room["occupants"])

        if total_capacity > 0:
            occupancy_rate = (total_occupied / total_capacity) * 100
        else:
            occupancy_rate = 0

        print(
            f"{block_name}: "
            f"{total_occupied}/{total_capacity} occupied "
            f"({occupancy_rate:.1f}%)"
        )


# ============================================================
# (b) STUDENT REGISTRATION AND ROOM ALLOCATION
# ============================================================

def register_student():
    """Register a student and allocate the student to a room."""

    print("\n" + "=" * 60)
    print("STUDENT REGISTRATION AND ROOM ALLOCATION")
    print("=" * 60)

    # Student registration number
    while True:
        reg_no = input("Enter student registration number: ").strip()

        if not reg_no:
            print("Registration number cannot be empty.")
        elif reg_no in students:
            print("A student with this registration number already exists.")
        else:
            break

    # Student name
    while True:
        name = input("Enter student name: ").strip()

        if not name:
            print("Student name cannot be empty.")
        else:
            break

    # Select block
    while True:
        print("\nAvailable hostel blocks:")

        for block_name in hostel_blocks:
            print("-", block_name)

        block_name = input("Enter hostel block: ").strip()

        if block_name in hostel_blocks:
            break

        print("Invalid block. Please choose one of the available blocks.")

    # Select room
    while True:
        print(f"\nAvailable rooms in {block_name}:")

        for room_name, room in hostel_blocks[block_name]["rooms"].items():
            occupied = len(room["occupants"])
            capacity = room["capacity"]

            print(f"{room_name}: {occupied}/{capacity} occupied")

        room_number = input("Enter room number: ").strip()

        if room_number not in hostel_blocks[block_name]["rooms"]:
            print("Invalid room number. Please select an existing room.")
            continue

        room = hostel_blocks[block_name]["rooms"][room_number]

        if len(room["occupants"]) >= room["capacity"]:
            print(
                f"Room {room_number} is already full. "
                f"Please select another room."
            )
            continue

        break

    # Hostel fee
    total_fee = get_positive_float("Enter total hostel fee: ")

    # Allocate student
    room["occupants"].append(reg_no)

    students[reg_no] = {
        "name": name,
        "block": block_name,
        "room": room_number,
        "total_fee": total_fee,
        "paid": 0.0,
        "balance": total_fee,
        "payments": []
    }

    save_data()

    print("\nStudent registered successfully.")
    print(f"Registration Number: {reg_no}")
    print(f"Name: {name}")
    print(f"Block: {block_name}")
    print(f"Room: {room_number}")
    print(f"Total Fee: {total_fee:,.2f}")
    print(f"Outstanding Balance: {total_fee:,.2f}")


# ============================================================
# (c) FEE PAYMENT RECORDING
# ============================================================

def record_payment():
    """Record a full or partial payment."""

    print("\n" + "=" * 60)
    print("RECORD FEE PAYMENT")
    print("=" * 60)

    reg_no = input("Enter student registration number: ").strip()

    if reg_no not in students:
        print("Student not found.")
        return

    student = students[reg_no]

    print(f"\nStudent: {student['name']}")
    print(f"Total Fee: {student['total_fee']:,.2f}")
    print(f"Amount Paid: {student['paid']:,.2f}")
    print(f"Outstanding Balance: {student['balance']:,.2f}")

    if student["balance"] <= 0:
        print("This student has already paid the full hostel fee.")
        return

    while True:
        amount = get_positive_float("Enter payment amount: ")

        if amount > student["balance"]:
            print(
                f"Payment cannot exceed the outstanding balance "
                f"of {student['balance']:,.2f}."
            )
        else:
            break

    # Update payment information
    student["paid"] += amount
    student["balance"] -= amount

    # Avoid small floating-point display errors
    student["balance"] = round(student["balance"], 2)
    student["paid"] = round(student["paid"], 2)

    student["payments"].append(amount)

    save_data()

    print("\nPayment recorded successfully.")
    print(f"Payment Made: {amount:,.2f}")
    print(f"Total Paid: {student['paid']:,.2f}")
    print(f"Outstanding Balance: {student['balance']:,.2f}")


# ============================================================
# (d) SEARCH STUDENT
# ============================================================

def search_student():
    """Search for a student by name or registration number."""

    print("\n" + "=" * 60)
    print("SEARCH STUDENT")
    print("=" * 60)

    keyword = input(
        "Enter student name or registration number: "
    ).strip().lower()

    if not keyword:
        print("Search value cannot be empty.")
        return

    found = False

    for reg_no, student in students.items(): #.items() gives us both the key and value together
                                            
        if (
            keyword in student["name"].lower()
            or keyword in reg_no.lower()
        ):

            found = True

            print("\nStudent Found")
            print("-" * 40)
            print(f"Registration Number: {reg_no}")
            print(f"Name: {student['name']}")
            print(f"Block: {student['block']}")
            print(f"Room: {student['room']}")
            print(f"Total Fee: {student['total_fee']:,.2f}")
            print(f"Amount Paid: {student['paid']:,.2f}")
            print(f"Balance: {student['balance']:,.2f}")

    if not found:
        print("No student matched your search.")


# ============================================================
# FULL OCCUPANCY REPORT
# ============================================================

def generate_occupancy_report():
    """Generate a detailed occupancy report for every hostel block."""

    print("\n" + "=" * 60)
    print("FULL HOSTEL OCCUPANCY REPORT")
    print("=" * 60)

    for block_name, block in hostel_blocks.items():

        rooms = block["rooms"]

        total_capacity = sum(
            room["capacity"] for room in rooms.values()
        )

        total_occupied = sum(
            len(room["occupants"]) for room in rooms.values()
        )

        if total_capacity > 0:
            occupancy_rate = (
                total_occupied / total_capacity
            ) * 100
        else:
            occupancy_rate = 0

        print(f"\n{block_name}")
        print("-" * 40)
        print(f"Number of rooms: {len(rooms)}")
        print(f"Total capacity: {total_capacity}")
        print(f"Total occupants: {total_occupied}")
        print(f"Occupancy rate: {occupancy_rate:.1f}%")

        print("\nRoom details:")

        for room_name, room in rooms.items():

            occupied = len(room["occupants"])
            capacity = room["capacity"]
            available = capacity - occupied

            print(
                f"  {room_name}: "
                f"{occupied}/{capacity} occupied, "
                f"{available} space available"
            )


# ============================================================
#  FEE DEFAULTERS
# ============================================================

def generate_fee_defaulters():
    """Display students whose balance is above a given threshold."""

    print("\n" + "=" * 60)
    print("FEE DEFAULTERS REPORT")
    print("=" * 60)

    threshold = get_non_negative_float(
        "Enter outstanding balance threshold: "
    )

    found = False

    print(
        f"\nStudents with outstanding balance above "
        f"{threshold:,.2f}:"
    )

    print("-" * 60)

    for reg_no, student in students.items():

        if student["balance"] > threshold:

            found = True

            print(f"Registration Number: {reg_no}")
            print(f"Name: {student['name']}")
            print(f"Block: {student['block']}")
            print(f"Room: {student['room']}")
            print(f"Outstanding Balance: {student['balance']:,.2f}")
            print("-" * 60)

    if not found:
        print("No students were found above the specified threshold.")


# ============================================================
# (e) FILE PERSISTENCE
# ============================================================

def save_data():
    """Save hostel and student records to a JSON file."""

    data = {
        "hostel_blocks": hostel_blocks,
        "students": students
    }

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
            print("Data saved successfuly! ")

    except OSError as error:
        print(f"Warning: Could not save data. {error}")


def load_data():
    """Load saved data or create new data if the file is missing/damaged."""

    global hostel_blocks, students  #(global is required because this function assigns new values to 
                                          #hostel_blocks)

    if not os.path.exists(DATA_FILE):
        print("\nNo previous data file found.")
        print("Creating a new hostel data file...")

        data = create_hostel_data()

        hostel_blocks = data["hostel_blocks"]
        students = data["students"]

        save_data()
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        # Basic structure validation
        if (
            "hostel_blocks" not in data
            or "students" not in data
        ):
            raise ValueError("Invalid data structure.")

        hostel_blocks = data["hostel_blocks"]
        students = data["students"]

        print("\nSaved data loaded successfully.")

    except (
        json.JSONDecodeError,
        OSError,
        TypeError,
        ValueError,
        KeyError
    ):

        print("\nWarning: The saved data file is missing or damaged.")
        print("A new data file will be created.")

        data = create_hostel_data()

        hostel_blocks = data["hostel_blocks"]
        students = data["students"]

        save_data()


# ============================================================
# (f) MENU-DRIVEN DRIVER PROGRAMME
# ============================================================

def display_menu():

    print("\n" + "=" * 60)
    print("HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM")
    print("=" * 60)

    print("1. Register student and allocate room")
    print("2. Record fee payment")
    print("3. Search student")
    print("4. View detailed occupancy report")
    print("5. View fee defaulters")
    print("6. View occupancy overview")
    print("7. Save & Exit")

    print("=" * 60)


def main():

    # Load saved records when the programme starts
    load_data()
    print_occupancy_overview()       # Print occupancy overview when programme starts
      
                                
    while True:

        display_menu()

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            register_student()

        elif choice == "2":
            record_payment()

        elif choice == "3":
            search_student()

        elif choice == "4":
            generate_occupancy_report()

        elif choice == "5":
            generate_fee_defaulters()

        elif choice == "6":
            print_occupancy_overview()

        elif choice == "7":
            print("\nThank you for using the Hostel Management System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")



if __name__ == "__main__":
    main()

