import frappe
from frappe.utils import today, add_days, getdate, formatdate  # type: ignore

def execute(filters):
    today_date = getdate(today())

    # Get filter values for from_date and to_date
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    # Ensure from_date and to_date are datetime.date objects
    if from_date:
        from_date = getdate(from_date)
    else:
        from_date = today_date

    if to_date:
        to_date = getdate(to_date)
    else:
        to_date = add_days(today_date, 7)  # Default to 7 days range

    # Fetch active employees with date_of_birth
    data = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["employee_name", "date_of_birth"],
    )

    # Filter employees and format date & day
    filtered_data = []
    for emp in data:
        if not emp["date_of_birth"]:
            continue  # Skip if date_of_birth is missing

        birth_date = getdate(emp["date_of_birth"])

        try:
            # Construct birthday in the current year
            birthday_this_year = getdate(f"{today_date.year}-{birth_date.month}-{birth_date.day}")
        except ValueError:
            # Handle leap year issue (e.g., Feb 29 in a non-leap year)
            if birth_date.month == 2 and birth_date.day == 29:
                # If it's Feb 29, set the birthday to Feb 28 in a non-leap year
                birthday_this_year = getdate(f"{today_date.year}-02-28")
            else:
                continue  # Skip if the birth date is invalid for the current year

        # Check if the birthday falls within the given range
        if from_date <= birthday_this_year <= to_date:
            filtered_data.append({
                "employee_name": emp["employee_name"],
                "day": birthday_this_year.strftime("%A"),  # Get weekday name
                "date": birthday_this_year,  # Display in "YYYY-MM-DD" format
                "count": 1,
            })

    # Define columns
    columns = [
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "day", "label": "Day", "fieldtype": "Data", "width": 120},
        {"fieldname": "date", "label": "Date (This Year)", "fieldtype": "Date", "width": 120},
        {"fieldname": "count","fieldtype": "Int","label": "Count","hidden": 1,"width": "120"},
    ]

    return columns, filtered_data
