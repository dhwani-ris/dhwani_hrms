frappe.ui.form.on("Attendance", {
    refresh: function (frm) {
        customBreadCrumbs.add(frm.doctype, "Form", "My Attendance")
      }
});

