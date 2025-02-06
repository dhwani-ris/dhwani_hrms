frappe.listview_settings["Attendance Request"] = {
	hide_name_column: true,
	hide_name_filter: true,

	onload: function (list_view) {	
		customBreadCrumbs.add(list_view.doctype,"List", "My Attendance")
	},

	
};

