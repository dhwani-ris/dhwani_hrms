frappe.listview_settings["Timesheet"] = {
	hide_name_column: true, // this part
	hide_name_filter: true,

	add_fields: ["status", "total_hours", "start_date", "end_date"],
	get_indicator: function (doc) {
		if (doc.status == "Billed") {
			return [__("Billed"), "green", "status,=," + "Billed"];
		}

		if (doc.status == "Payslip") {
			return [__("Payslip"), "green", "status,=," + "Payslip"];
		}

		if (doc.status == "Completed") {
			return [__("Completed"), "green", "status,=," + "Completed"];
		}
	},
	onload: function (listview) {
		customBreadCrumbs.add(listview.doctype, "List", "All Timesheet")
	},
	
}