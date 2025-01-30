import frappe

#dhwani_hrms.dhwani_hrms.custom_number_cards.work_anniversary_card.get_upcoming_work_anniversary
@frappe.whitelist(allow_guest=True)
def get_upcoming_work_anniversary():
    report = frappe.get_doc("Report", "Work Anniversary")
    from_date = frappe.utils.nowdate()
    to_date = frappe.utils.get_last_day(from_date)  # Get last date of the current month
    
    columns, data = report.get_data(
        filters={"from_date": from_date, "to_date": to_date}, as_dict=True
    )
    
    values = data[-1].get("count") if data else 0
    
    return {
        "value": values,
        "fieldtype": "Int",
        "route_options": {
            "from_date": from_date,
            "to_date": to_date,
        },
        "route": ["query-report", "Work Anniversary"],
    }
