import frappe
from frappe import _


def execute(filters=None):
    # If no filters are provided, set them to an empty dictionary
    if not filters:
        filters = {}

    # Apply year filter if provided
    if filters.get("year"):
        filters["holiday_date"] = [
            "between",
            [f"{filters.get('year')}-01-01", f"{filters.get('year')}-12-31"],
        ]
        del filters["year"]

    filters["weekly_off"] = 0  # Exclude weekly offs
    holidays = frappe.get_all(
        "Holiday",
        fields=["name", "holiday_date", "description"],
        filters=filters,
        order_by="holiday_date asc",
    )

    holiday_data = []
    for holiday in holidays:
        holiday_date = frappe.utils.getdate(holiday.holiday_date)
        day_name = holiday_date.strftime("%A")

        holiday_data.append(
            {
                # "name": holiday.name,
                "holiday_date": holiday.holiday_date,
                "day": day_name,  # Include day name
                "description": holiday.description,
            }
        )

    columns = [
        _("Holiday Date") + ":Date:120",
        _("Day") + ":Data:100",  # Add Day column
        _("Description") + ":Data:200",
    ]

    return columns, holiday_data
