frappe.listview_settings["Compensatory Leave Request"] = {
    hide_name_column: true,
	hide_name_filter: true,
	onload: function (listview) {
        customBreadCrumbs.add(listview.doctype,"List", "Leave")
    },
};
