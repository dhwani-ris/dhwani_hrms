import frappe

from frappe import _
from frappe.utils import cint


# # dhwani_hrms.dhwani_hrms.api.employee_checkin.add_log
# @frappe.whitelist(allow_guest=True)
# def add_log(
#     employee_field_value,
#     timestamp,
#     device_id=None,
#     log_type=None,
#     skip_auto_attendance=0,
#     employee_fieldname="attendance_device_id",
# ):
#     """Finds the relevant Employee using the employee field value and creates a Employee Checkin.

#     :param employee_field_value: The value to look for in employee field.
#     :param timestamp: The timestamp of the Log. Currently expected in the following format as string: '2019-05-08 10:48:08.000000'
#     :param device_id: (optional)Location / Device ID. A short string is expected.
#     :param log_type: (optional)Direction of the Punch if available (IN/OUT).
#     :param skip_auto_attendance: (optional)Skip auto attendance field will be set for this log(0/1).
#     :param employee_fieldname: (Default: attendance_device_id)Name of the field in Employee DocType based on which employee lookup will happen.
#     """

#     if not employee_field_value or not timestamp:
#         frappe.throw(_("'employee_field_value' and 'timestamp' are required."))

#     employee = frappe.db.get_values(
#         "Employee",
#         {employee_fieldname: employee_field_value},
#         ["name", "employee_name", employee_fieldname],
#         as_dict=True,
#     )
#     if employee:
#         employee = employee[0]
#     else:
#         frappe.throw(
#             _("No Employee found for the given employee field value. '{}': {}").format(
#                 employee_fieldname, employee_field_value
#             )
#         )

#     doc = frappe.new_doc("Employee Checkin")
#     doc.employee = employee.name
#     doc.employee_name = employee.employee_name
#     doc.time = timestamp
#     doc.device_id = device_id
#     doc.log_type = log_type
#     if cint(skip_auto_attendance) == 1:
#         doc.skip_auto_attendance = "1"
#     doc.insert(ignore_permissions=True)

#     return doc


# https://stgfrappe.dhwaniris.in/api/method/dhwani_hrms.dhwani_hrms.api.employee_checkin.add_log
@frappe.whitelist(allow_guest=True)
def add_log(**kwargs):
    try:
        kwargs.pop("cmd")
        e_checkin = frappe.new_doc("Employee Checkin Log")
        e_checkin.data = kwargs
        e_checkin.insert(
            ignore_permissions=True,
        )
        return e_checkin.name
    except Exception as e:
        frappe.log_error(e)
        return str(e)
