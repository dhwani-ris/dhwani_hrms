frappe.listview_settings["Project"] = {
	hide_name_column: true, // this part
	add_fields: ["status", "priority", "is_active", "percent_complete", "expected_end_date", "project_name"],
	filters: [["status", "=", "Open"]],
	get_indicator: function (doc) {
		if (doc.status == "Open" && doc.percent_complete) {
			return [__("{0}%", [cint(doc.percent_complete)]), "orange", "percent_complete,>,0|status,=,Open"];
		} else {
			return [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		}
	},
	refresh: function(listview) {
		$("use.like-icon").hide();
 },
 onload: function (listview) {
	 customBreadCrumbs.add(listview.doctype, "List", "All Timesheet")
 },
}