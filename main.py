# main.py
"""
Malaysian Tax Input Program - Main Module
Author: <Your Name>
Course: SQITK 3073 Business Analytic Programming

Features:
- Registration and login using IC + last 4 digits as password
- Tax calculation
- Save/read CSV with pandas
"""

from functions import verify_user, calculate_tax, save_to_csv, read_from_csv

FILENAME = "tax_records.csv"


def get_float(prompt: str) -> float:
    """Utility to safely get float input with validation."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def main():
    print("=== Malaysian Tax Input Program ===")

    existing_df = read_from_csv(FILENAME)
    registered_ics = set(existing_df["IC_Number"]) if existing_df is not None else set()

    while True:
        ic_number = input("Enter IC Number (12 digits): ").strip()
        password = input("Enter Password (last 4 digits of IC): ").strip()

        if verify_user(ic_number, password):
            if ic_number not in registered_ics:
                print("\nIC not found. New user registration:")
                user_id = input("Create User ID: ").strip()
                confirm_pw = input("Re-enter Password (last 4 digits of IC): ").strip()

                if confirm_pw != password:
                    print("Passwords do not match. Registration failed.\n")
                    continue

                print("Registration successful!\n")
            else:
                print("\nWelcome back!")
                user_id = input("Enter User ID: ").strip()

            # Income + relief inputs
            income = get_float("Enter Annual Income (RM): ")
            tax_relief = get_float("Enter Total Tax Relief (RM): ")

            # Calculate tax
            tax_payable = calculate_tax(income, tax_relief)
            print(f"\nChargeable Income: RM {max(0, income - tax_relief):,.2f}")
            print(f"Tax Payable: RM {tax_payable:,.2f}\n")

            # Save record
            record = {
                "User_ID": user_id,
                "IC_Number": ic_number,
                "Annual_Income": income,
                "Tax_Relief": tax_relief,
                "Tax_Payable": tax_payable
            }
            save_to_csv(record, FILENAME)
            print("Record saved successfully.\n")

            # Menu loop
            while True:
                print("1. View All Tax Records")
                print("2. Calculate Another Tax")
                print("3. Exit")
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    df = read_from_csv(FILENAME)
                    print("\n=== Tax Records ===")
                    print(df.to_string(index=False) if df is not None else "No records found.")
                    print()
                elif choice == "2":
                    break
                elif choice == "3":
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice. Try again.\n")
        else:
            print("Invalid IC or password. Please try again.\n")


if __name__ == "__main__":
    main()
