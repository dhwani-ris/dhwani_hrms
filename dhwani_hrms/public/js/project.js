frappe.ui.form.on("Project", {
    refresh(frm) {
        const read_only_roles = ["Administrator", "HR Manager", "Project Manager"];
        const current_user_roles = frappe.user_roles;

        const is_read_only = !read_only_roles.some(role => current_user_roles.includes(role));

        // Iterate through all fields and set read_only based on user role
        for (let fieldname in frm.fields_dict) {
            const field = frm.fields_dict[fieldname];
            // Check if the field exists and is not already read_only by default
            if (field && !field.df.read_only) { 
                frm.set_df_property(fieldname, "read_only", is_read_only ? 1 : 0);
            }
        }
    }
});
