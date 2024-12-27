frappe.listview_settings["Employee"] = {
	hide_name_column: true, // this part
	hide_name_filter: true,
	add_fields: ["status", "branch", "department", "designation", "image"],
	filters: [["status", "=", "Active"]],
	get_indicator: function (doc) {
		var indicator = [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		indicator[1] = { Active: "green", Inactive: "red", Left: "gray", Suspended: "orange" }[doc.status];
		return indicator;
	},
}