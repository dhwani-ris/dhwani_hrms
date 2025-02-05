import frappe
import datetime
from frappe.utils import cint, flt, getdate, date_diff
from frappe import _
from hrms.hr.doctype.leave_application.leave_application import (
    get_holidays,
)
from dhwani_hrms.dhwani_hrms.utils.custom_send_email import send_email_notification  # Import the common function


def validate(doc, method):
    if doc.reason == "Work From Home":
        if (
            doc.custom_wfh_allowance_used__this_month_ + doc.custom_total_applied_days
        ) > float(doc.custom_work_from_home_allowance_this_month):
            frappe.throw(
                _("Insufficient balance for Work From Home Allowance"),
                title=_("Insufficient Balance"),
            )


def on_submit(doc, method):
    if doc.reason == "Work From Home":
        frappe.db.set_value(
            "Employee",
            doc.employee,
            "custom_wfh_allowance_used",
            float(
                doc.custom_wfh_allowance_used__this_month_
                + doc.custom_total_applied_days
            ),
        )
        frappe.db.commit()


def on_cancel(doc, method):
    frappe.db.set_value(
        "Employee",
        doc.employee,
        "custom_wfh_allowance_used",
        doc.custom_total_applied_days,
    )

def on_update(doc, method):
    if doc.workflow_state == "Review":
        reports_to = frappe.get_value("Employee", doc.employee, ["reports_to"])
        leave_approver_name,leave_approver_email = frappe.get_value("Employee", reports_to, ["employee_name","company_email"])
        
        if not leave_approver_email:
            frappe.throw("Leave Approver is not set for this employee", title="Approver Not Found")
        
        leave_approver_name = frappe.get_value("Employee", reports_to, "employee_name")
        send_email_notification(doc, leave_approver_email, "Approval Request", leave_approver_name)
        
def on_cancel(doc, method):
    if doc.workflow_state == "Rejected":
        send_email_notification(doc, doc.owner, "Cancellation",doc.employee_name)
        
def on_update_after_submit(doc, method):  
    send_email_notification(doc, doc.owner, "Approval",doc.employee_name)

# dhwani_hrms.dhwani_hrms.doc_events.attendance_request.get_number_of_leave_days
@frappe.whitelist()
def get_number_of_leave_days(
    employee: str,
    from_date: datetime.date,
    to_date: datetime.date,
    half_day: int | str | None = None,
    half_day_date: datetime.date | str | None = None,
    holiday_list: str | None = None,
) -> float:
    """Returns number of leave days between 2 dates after considering half day and holidays
    (Based on the include_holiday setting in Leave Type)"""
    number_of_days = 0
    if cint(half_day) == 1:
        if getdate(from_date) == getdate(to_date):
            number_of_days = 0.5
        elif half_day_date and getdate(from_date) <= getdate(half_day_date) <= getdate(
            to_date
        ):
            number_of_days = date_diff(to_date, from_date) + 0.5
        else:
            number_of_days = date_diff(to_date, from_date) + 1
    else:
        number_of_days = date_diff(to_date, from_date) + 1

    number_of_days = flt(number_of_days) - flt(
        get_holidays(employee, from_date, to_date, holiday_list=holiday_list)
    )
    return number_of_days
