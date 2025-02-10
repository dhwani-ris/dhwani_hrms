frappe.listview_settings["Leave Application"] = {
	hide_name_column: true,
	hide_name_filter: true,

	onload: function (list_view) {	
		customBreadCrumbs.add(list_view.doctype,"List", "Leave")
	},

	
};

