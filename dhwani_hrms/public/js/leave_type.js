frappe.ui.form.on("Leave Application", {
    from_date: function (frm) {
        // Temporary flag to ensure the message is shown only once per interaction
        if (!frm.__from_date_alert_shown) {
            frm.__from_date_alert_shown = true; // Set flag

            if (!frm.doc.leave_type) {
                if (frm.doc.from_date) {
                    frm.set_value("from_date", null); // Clear the "from_date"
                }
                frappe.msgprint(__("Please select a Leave Type before setting the From Date."));
            } else {
                leaveRestriction(frm); // Execute your custom function
            }
            // Reset the flag after a short delay (optional, to allow retries)
            setTimeout(() => {
                frm.__from_date_alert_shown = false; // Reset flag
            }, 500); // Adjust delay as needed
        }
    },
    leave_type: function(frm) {
        // Check if "from_date" is filled
        if (frm.doc.from_date) {
            // Set a flag to prevent "from_date" function execution
            frm.__skip_from_date_function = true;

            // Clear the "from_date" field
            frm.set_value("from_date", null).then(() => {
                frm.__skip_from_date_function = false; 
            });
        }
    },
});
function leaveRestriction(frm){
    if (frm.doc.leave_type) {
        frappe.db.get_value("Leave Type", {name: frm.doc.leave_type}, ["custom_apply_casual_leave_before_days","custom_days","custom_past_day_submition_not_allowed"])
            .then((value)=>{
                if(value && value.message.custom_apply_casual_leave_before_days || value.message.custom_past_day_submition_not_allowed){
                    let days = value.message.custom_apply_casual_leave_before_days;
                    let past_day = value.message.custom_past_day_submition_not_allowed
                    validateTime(frm, 'from_date', value.message.custom_days, frm.doc.leave_type,past_day);
                }
            });
        }
    
}
function validateTime(frm, fieldname, custom_days, leave_type,past_day) {
    const selected_date = moment(frm.doc[fieldname]); // Parse selected date
    const today = moment().startOf('day'); // Get today's date
    const min_days = moment().add(custom_days-1, 'days'); // Minimum days before leave can be applied
    if (past_day == 1) {
        if (selected_date.isBefore(today)) {
            if(frm.doc.from_date){
                frappe.msgprint(__("You cannot apply for leave on past dates."));
            }
            frm.set_value("from_date", null);
            return;
        }
        if (leave_type === "Casual Leave" || leave_type === "Privilege Leave" || leave_type==="Compensatory Off" || leave_type==="Sick Leave") {

            if (selected_date.isBefore(min_days)) {
                if(frm.doc.from_date){
                    frappe.msgprint(__("You must apply for " + leave_type + " at least " + custom_days + " days in advance."));
                }
                frm.set_value("from_date", null);
                return;
            }
        }
    }
}
