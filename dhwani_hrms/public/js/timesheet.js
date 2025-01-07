// Copyright (c) 2016, Dhwani RIS Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Timesheet", {
	refresh: function (frm) {
        // 
	},
});

frappe.ui.form.on("Timesheet Detail", {

    from_time: function (frm, cdt, cdn) {
		frappe.db.get_value("Timesheet Settings", {name: 'Timesheet Settings'}, ["limit_older_timesheets"]).then((value)=>{
            if(value && value.message.limit_older_timesheets){
					validateTime(frm, cdt, cdn, 'from_time', value.message.older_days, value.message.future_days);
            }
        })
    },

    to_time: function(frm, cdt, cdn) {
		frappe.db.get_value("Timesheet Settings", {name: 'Timesheet Settings'}, ["limit_older_timesheets"]).then((value)=>{
            if(value && value.message.limit_older_timesheets){
				validateTime(frm, cdt, cdn, 'to_time', value.message.older_days, value.message.future_days); // Pass 'to_time' here
            }
        })
    }
});


function validateTime(frm, cdt, cdn, fieldname, older_days, future_days) {
    let row = locals[cdt][cdn];
    const time = moment(row[fieldname]);
    const past_limit = moment().subtract(older_days, 'days');
    const future_limit = moment().add(future_days, 'days');

    if (time.isBefore(past_limit)) {
        frappe.msgprint(__("You cannot select a " + fieldname + " older than " + older_days + " weeks in the past"));
        frappe.model.set_value(cdt, cdn, fieldname, null);
        return; 
    }

    if (time.isAfter(future_limit)) {
        frappe.msgprint(__("You cannot select a " + fieldname + " more than " + future_days + " weeks in the future."));
        frappe.model.set_value(cdt, cdn, fieldname, null);
        return;
    }
}







frappe.db.get_value("Timesheet Settings", {name: 'Timesheet Settings'}, ["limit_older_timesheets"]).then((value)=>{
            // This part seems unrelated to the two-week validation, but preserving it as is.
            if(value){
                if(value.message.limit_older_timesheets){
					//Existing logic if needed
				}
            }
        })