import frappe

def before_save(doc, method):
    if doc.custom_employee_no:
        doc.employee_number = doc.custom_employee_no  # Assign value directly
        doc.name = doc.custom_employee_no
    else:
        frappe.throw("Please enter Employee Number")  # Ensure custom_employee_no is filled

