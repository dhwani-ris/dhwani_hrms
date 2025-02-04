frappe.ui.form.on("Compensatory Leave Request", {
    refresh(frm) {

        customBreadCrumbs.add(frm.doctype, "Form", "Leave")
    },
});
