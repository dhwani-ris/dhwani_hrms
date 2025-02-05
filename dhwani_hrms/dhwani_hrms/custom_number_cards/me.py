import frappe


# dhwani_hrms.dhwani_hrms.custom_number_cards.me.get_current_user_timesheet
@frappe.whitelist()
def get_current_user_timesheet():
    user = frappe.session.user
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    timesheet_count = frappe.db.count("Timesheet", filters={"employee": employee})
    return {
        "value": timesheet_count,
        "fieldtype": "int",
        "route_options": {"employee": employee},
        "route": ["List", "Timesheet"],
    }


# dhwani_hrms.dhwani_hrms.custom_number_cards.me.get_current_user_leaves
@frappe.whitelist()
def get_current_user_leaves():
    user = frappe.session.user
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    leave_count = frappe.db.count("Leave Application", filters={"employee": employee})
    return {
        "value": leave_count,
        "fieldtype": "int",
        "route_options": {"employee": employee},
        "route": ["List", "Leave Application"],
    }
