$(document).ready(function () {
    // Target the Navbar link for "My Profile"
    $(".navbar .dropdown-item").each(function () {
        if ($(this).text().trim() === "My Profile") {
            $(this).on("click", function (event) {
                event.preventDefault(); // Prevent default link behavior

                // Make an API call to get the current user's Employee ID
                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Employee",
                        filters: { user_id: frappe.session.user },
                        fieldname: "name"
                    },
                    callback: function (response) {
                        if (response.message) {
                            let employee_id = response.message.name;
                            if (employee_id) {
                                // Redirect to the employee profile  
                                window.location.href = `/app/employee/${employee_id}`;
                            } else {
                                frappe.msgprint("Employee profile not found.");
                            }
                        }
                    }
                });
            });
        }
    });
});
