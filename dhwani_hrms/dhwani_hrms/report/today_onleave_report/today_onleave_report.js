frappe.query_reports["Today OnLeave Report"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(), // Set default as today's date
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(), // Set default as today's date
        },
        {
            fieldname: "leave_type",
            label: __("Leave Type"),
            fieldtype: "Select",
            options: [], // Leave type options
            default: "", // Default to show all leave types
        }
    ],
	// Fetch leave types dynamically before rendering the report
    onload: function (report) {
        frappe.call({
            method: "frappe.client.get_list", // Frappe method to fetch data from server
            args: {
                doctype: "Leave Type",
                fields: ["name"],
            },
            callback: function (response) {
                if (response.message) {
                    // Add leave type options dynamically
                    let leave_type_options = [""].concat(
                        response.message.map((lt) => lt.name)
                    );

                    // Update the leave_type filter
                    report.page.fields_dict.leave_type.df.options = leave_type_options;
                    report.page.fields_dict.leave_type.refresh();
                }
            },
        });
    },
}


