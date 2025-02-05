frappe.listview_settings["Employee Checkin"] = {
    hide_name_column: true,
	hide_name_filter: true,
	onload: function (listview) {
		customBreadCrumbs.add(listview.doctype,"List", "My Attendance")
		listview.page.add_action_item(__("Fetch Shifts"), () => {
			const checkins = listview.get_checked_items().map((checkin) => checkin.name);
			frappe.call({
				method: "hrms.hr.doctype.employee_checkin.employee_checkin.bulk_fetch_shift",
				freeze: true,
				args: {
					checkins,
				},
			});
		});
	},
};
