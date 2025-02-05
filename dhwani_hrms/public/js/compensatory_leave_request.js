frappe.ui.form.on("Compensatory Leave Request", {
    refresh(frm) {
        customBreadCrumbs.add(frm.doctype, "Form", "Leave");

        if (!(frappe.user.has_role("HR Manager") || frappe.user.has_role("HR User") || frappe.user.has_role("System Manager"))) {
            frm.set_query("employee", () => ({
                filters: {
                    user_id: frappe.session.user
                }
            }));
        }
    }
});
