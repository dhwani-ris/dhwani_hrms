frappe.ui.form.on("Employee", {
    refresh(frm) {
        const read_only_roles = ["Administrator","System Manager", "HR User", "HR Manager"]; 
        const current_user_roles = frappe.user_roles;

        if (!read_only_roles.some(role => current_user_roles.includes(role))) { 
            frm.set_df_property("custom_work_from_home_allowance", "read_only", 1);
        } else {
            frm.set_df_property("custom_work_from_home_allowance", "read_only", 0);
        }



    },
});

