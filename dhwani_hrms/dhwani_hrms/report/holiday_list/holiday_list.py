# holiday_list.py (Script Report)

import frappe
from frappe import _


def execute(filters=None):
    # If no filters are provided, set them to an empty dictionary
    if not filters:
        filters = {}

    # Fetch holidays from the Holiday doctype
    filters["weekly_off"] = 0
    holidays = frappe.get_all(
        "Holiday",
        fields=["name", "holiday_date", "description"],
        filters=filters,
        order_by="holiday_date asc",
    )

    # Prepare a list of dictionaries to pass to the report
    holiday_data = []
    for holiday in holidays:
        holiday_data.append(
            {
                "name": holiday.name,
                "holiday_date": holiday.holiday_date,
                "description": holiday.description,
            }
        )

    # Define columns for the report (fields to display)
    columns = [
        _("Holiday Date") + ":Date:120",
        _("Description") + ":Data:200",
    ]

    # Return the data and columns for the report
    return columns, holiday_data
