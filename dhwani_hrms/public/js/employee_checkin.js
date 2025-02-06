frappe.ui.form.on("Employee Checkin", {
    refresh(frm) {

        customBreadCrumbs.add(frm.doctype, "Form", "My Attendance")
    
        frappe.call({
            method: "dhwani_hrms.dhwani_hrms.api.employee_checkin_attendence.get_attendance_request",
            args: { user: frappe.session.user },
            callback: function(response) {
                if (response.message && !response.message.error) {
                    let attendance = response.message;
                    if (attendance.reason === "Work From Home" ) {
                        frm.set_df_property("log_type", "read_only", 0); // Editable
                    } else {
                        frm.set_df_property("log_type", "read_only", 1); // Read-only
                    }
                } else {
                    frm.set_df_property("log_type", "read_only", 1); // No valid Attendance Request found
                }
            }
        });
    }
    
    
    
    
    




});

