import frappe

frappe.ui.form.on("Leave Application", {
    from_date: function (frm) {
        # Check if the leave type is "Casual Leave" or "Sick Leave"
        if (frm.doc.leave_type === "Casual Leave" || frm.doc.leave_type === "Sick Leave") {
            frappe.db.get_value("Leave Type", { name: frm.doc.leave_type }, ["custom_apply_casual_leave_before_days"])
                .then((value) => {
                    if (value && value.message.custom_apply_casual_leave_before_days) {
                        validateDate(frm, 'from_date', value.message.custom_apply_casual_leave_before_days);
                    }
                });
        }
    }
});

function validateDate(frm, fieldname, custom_days) {
    const date = moment(frm.doc[fieldname]);
    const past_limit = moment().subtract(custom_days, 'days');

    if (date.isBefore(past_limit)) {
        frappe.msgprint(__("You cannot select a " + fieldname + " older than " + custom_days + " days in the past"));
        frm.set_value(fieldname, null);
        return;
    }
}
