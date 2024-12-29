import frappe
import calendar
from datetime import date, timedelta, datetime
from frappe import _

# TODO: Add Holiday List status in the code

STATUS_LIST = ["Weekoff", "Present", "Absent", "Leave", "Work From Home"]


def execute(filters=None):
    data, chart = get_data(filters)
    report_summary = get_report_summary(data)

    # Include chart in the return values
    return get_columns(filters=filters), data, None, chart, report_summary


def get_columns(filters=None):
    if not filters:
        filters = {}

    month = filters.get("month")
    year = int(filters.get("year"))

    month_number = list(calendar.month_name).index(month)
    num_days = calendar.monthrange(year, month_number)[1]

    columns = [
        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150,
        },
        {
            "fieldname": "employee_name",
            "label": "Employee Name",
            "fieldtype": "Data",
            "width": 150,
        },
    ]

    # Prepare the date columns for the entire month
    current_date = date(year, month_number, 1)
    for _ in range(num_days):
        date_str = current_date.strftime("%Y-%m-%d")
        columns.append(
            {
                "fieldname": date_str,
                "label": current_date.strftime("%d-%m-%Y"),
                "fieldtype": "Data",
                "indicator": "red",
                "width": 200,
            }
        )
        current_date += timedelta(days=1)

    return columns


def get_report_summary(data):
    if not data:
        return None

    status_counts = {
        "Present": 0,
        "Absent": 0,
        "Leave": 0,
        "Work From Home": 0,
        "Weekoff": 0,
    }

    for row in data:
        for date_str, status in row.items():
            if isinstance(status, str):
                if status in status_counts:
                    status_counts[status] += 1
                elif "Leave" in status:
                    status_counts["Leave"] += 1
                elif "Work From Home" in status:
                    status_counts["Work From Home"] += 1

    summary = []
    for status, count in status_counts.items():
        indicator = "Gray"  # Default
        if status == "Present":
            indicator = "Green"
        elif status == "Absent":
            indicator = "Red"
        elif status == "Leave":
            indicator = "Orange"
        elif status == "Work From Home":
            indicator = "Purple"
        # Weekoff already handles by default

        summary.append(
            {
                "value": count,
                "indicator": indicator,
                "label": _(status),
                "datatype": "Int",
            }
        )

    return summary


def get_data(filters):
    month = filters.get("month")
    year = int(filters.get("year"))
    employee = filters.get("employee")  # Get the employee filter
    month_number = list(calendar.month_name).index(month)
    num_days = calendar.monthrange(year, month_number)[1]

    conditions = "WHERE status='Active'"
    if employee:
        conditions += f" AND name={employee}"

    emp_template = f"""
        SELECT name, employee_name 
        FROM `tabEmployee` 
        {conditions} 
        """
    employees = frappe.db.sql(
        emp_template,
        as_dict=True,
    )

    date_list = [
        (
            date(year, month_number, day).strftime("%Y-%m-%d"),
            date(year, month_number, day).strftime("%d-%m-%Y"),
        )
        for day in range(1, num_days + 1)
    ]

    attendance_data = get_attendance_data(year, month_number, num_days, employees)
    leave_data = get_leave_data(year, month_number, num_days, employees)
    wfh_data = get_wfh_data(year, month_number, num_days, employees)

    data = []
    for employee in employees:
        row = {"employee": employee.name, "employee_name": employee.employee_name}
        for date_str, date_label in date_list:
            status_dict = get_employee_status(
                employee.name, date_str, attendance_data, leave_data, wfh_data
            )
            row[date_str] = status_dict.get("status")

        data.append(row)

    chart = get_chart_data(data)
    return data, chart


def get_chart_data(data):
    if not data:
        return None

    status_counts = {}
    for row in data:
        for date_str, status in row.items():
            if status and any(item in status for item in STATUS_LIST):
                if isinstance(status, str):  # Check if it's a string
                    status_counts.setdefault(status, 0)
                    status_counts[status] += 1
                elif (
                    isinstance(status, dict) and "status" in status
                ):  # check if it is a dictionary
                    status_str = status.get("status")
                    status_counts.setdefault(status_str, 0)
                    status_counts[status_str] += 1

    labels = list(status_counts.keys())
    chart = {
        "data": {
            "labels": labels,
            "datasets": [{"name": _("Status"), "values": list(status_counts.values())}],
        },
        "type": "percentage",
        "height": 300,
    }
    return chart


def get_attendance_data(year, month_number, num_days, employees):
    if not employees:  # Handle the case where no employees are active
        return []

    if len(employees) == 1:  # Handle single employee case
        employee_condition = f"employee = '{employees[0]['name']}'"
    else:
        employee_condition = f"employee IN {tuple([emp['name'] for emp in employees])}"

    return frappe.db.sql(
        f"""
			SELECT employee, attendance_date, status
			FROM `tabAttendance`
			WHERE attendance_date BETWEEN '{year}-{month_number:02d}-01' AND '{year}-{month_number:02d}-{num_days:02d}'
			AND {employee_condition}
		""",
        as_dict=True,
    )


def get_leave_data(year, month_number, num_days, employees):
    if not employees:
        return []

    if len(employees) == 1:
        employee_condition = f"employee = '{employees[0]['name']}'"
    else:
        employee_condition = f"employee IN {tuple([emp['name'] for emp in employees])}"

    return frappe.db.sql(
        f"""
			SELECT employee, from_date, to_date, leave_type, half_day
			FROM `tabLeave Application`
			WHERE docstatus != 2 AND from_date <= '{year}-{month_number:02d}-{num_days:02d}' AND to_date >= '{year}-{month_number:02d}-01'
			AND {employee_condition}
		""",
        as_dict=True,
    )


def get_wfh_data(year, month_number, num_days, employees):
    if not employees:
        return []

    if len(employees) == 1:
        employee_condition = f"employee = '{employees[0]['name']}'"
    else:
        employee_condition = f"employee IN {tuple([emp['name'] for emp in employees])}"

    return frappe.db.sql(
        f"""
			SELECT employee, from_date, to_date, reason, half_day
			FROM `tabAttendance Request`
			WHERE reason='Work From Home'
			AND from_date <= '{year}-{month_number:02d}-{num_days:02d}' AND to_date >= '{year}-{month_number:02d}-01'
			AND {employee_condition}
		""",
        as_dict=True,
    )


def get_employee_status(employee, date_str, attendance_data, leave_data, wfh_data):
    current_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Check if it's a weekend
    if current_date.weekday() in (5, 6):  # 5 is Saturday, 6 is Sunday
        return {"status": "Weekoff", "color": "gray"}

    attendance = next(
        (
            a
            for a in attendance_data
            if a["employee"] == employee and a["attendance_date"] == current_date
        ),
        None,
    )
    if attendance:
        status = attendance["status"]
        color = (
            "green" if status == "Present" else "red"
        )  # Green for Present, Red for Absent
        return {
            "status": status,
            "color": color,
        }
    # Check leave status
    leave = next(
        (
            l
            for l in leave_data
            if l["employee"] == employee
            and l["from_date"] <= current_date <= l["to_date"]
        ),
        None,
    )
    if leave:
        leave_type = leave["leave_type"]
        half_day_text = " - Half Day" if leave["half_day"] else " - Full Day"

        return {"status": f"{leave_type}{half_day_text}", "color": "orange"}

    # Check Work From Home status
    wfh = next(
        (
            w
            for w in wfh_data
            if w["employee"] == employee
            and w["from_date"] <= current_date <= w["to_date"]
        ),
        None,
    )
    if wfh:
        reason = wfh["reason"]
        half_day_text = " - Half Day" if wfh["half_day"] else " - Full Day"
        return {"status": f"{reason}{half_day_text}", "color": "purple"}

    return {}
