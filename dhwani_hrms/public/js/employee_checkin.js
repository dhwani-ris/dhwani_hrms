frappe.ui.form.on("Employee Checkin", {
    refresh(frm) {

        customBreadCrumbs.add(frm.doctype, "Form", "My Attendance")
    },
});

