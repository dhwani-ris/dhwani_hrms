frappe.ui.form.on("Attendance Request", {
    refresh(frm){
        if (frm.is_new()) {
			frm.trigger("calculate_total_days");
		}
    },
    from_date: function (frm) {        
		frm.trigger("calculate_total_days");
	},
    to_date: function (frm) {         
        frm.trigger("calculate_total_days");
    },
    half_day: function (frm) {
        frm.trigger("calculate_total_days");
    },
    half_day_date: function (frm) {
        frm.trigger("calculate_total_days");
    },

    calculate_total_days: function (frm) {
		if (frm.doc.from_date && frm.doc.to_date && frm.doc.employee) {
			// server call is done to include holidays in leave days calculations
			return frappe.call({
				method: "dhwani_hrms.dhwani_hrms.doc_events.attendance_request.get_number_of_leave_days",
				args: {
					employee: frm.doc.employee,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
					half_day: frm.doc.half_day,
					half_day_date: frm.doc.half_day_date,
				},
				callback: function (r) {
                    console.log("wassuo", r.message);
                    
                    frm.set_value("custom_total_applied_days", r.message);
				},
			});
		}
	},
});


