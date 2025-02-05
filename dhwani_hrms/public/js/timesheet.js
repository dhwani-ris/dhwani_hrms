// Copyright (c) 2016, Dhwani RIS Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Timesheet", {
    refresh(frm){
        customBreadCrumbs.add(frm.doctype, "Form", "All Timesheet")
    },
    
});



frappe.ui.form.on("Timesheet Detail", {

    custom_date: function(frm, cdt, cdn) {
        frappe.db.get_value("Timesheet Settings", {name: 'Timesheet Settings'}, ["limit_older_timesheets"]).then((value)=>{
                    if(value && value.message.limit_older_timesheets){
            			validateCustomDate(frm, cdt, cdn, value.message.older_days, value.message.future_days); 
                    }
                })

        const row = locals[cdt][cdn];

        if (row.custom_date) {
            updateTimeFields(frm, cdt, cdn, row.custom_date); // Existing logic, if needed
        } else {
             frappe.model.set_value(cdt, cdn, 'from_time', null); // Clear dependent fields if date is cleared
             frappe.model.set_value(cdt, cdn, 'to_time', null);
        }
    },
});

function updateTimeFields(frm, cdt, cdn, custom_date) {
    let moment_date = moment(custom_date).startOf('day');

    let datetimeString = moment_date.format("YYYY-MM-DD HH:mm:ss");


    frappe.model.set_value(cdt, cdn, 'from_time', datetimeString);
    frappe.model.set_value(cdt, cdn, 'to_time', datetimeString);  
}





function validateCustomDate(frm, cdt, cdn, older_days, future_days) {
    let row = locals[cdt][cdn];
    const selectedDate = moment(row.custom_date);
    const pastLimit = moment().subtract(older_days, 'days');
    const futureLimit = moment().add(future_days, 'days');

    if (selectedDate.isBefore(pastLimit)) {
        frappe.msgprint(__("You cannot select a date older than " + older_days + " Days in the past"));
        frappe.model.set_value(cdt, cdn, 'custom_date', null); // Clear the invalid date
        frappe.model.set_value(cdt, cdn, 'from_time', null);
        frappe.model.set_value(cdt, cdn, 'to_time', null);
        return
    }
    if (selectedDate.isAfter(futureLimit)) {
        frappe.msgprint(__("You cannot select a date more than " + future_days + " Days in the future."));
        frappe.model.set_value(cdt, cdn, 'custom_date', null); // Clear the invalid date
        frappe.model.set_value(cdt, cdn, 'from_time', null);
        frappe.model.set_value(cdt, cdn, 'to_time', null);
        return
    }
}


function validateTime(frm, cdt, cdn, fieldname, older_days, future_days) {
    let row = locals[cdt][cdn];
    const time = moment(row[fieldname]);
    const past_limit = moment().subtract(older_days, 'days');
    const future_limit = moment().add(future_days, 'days');

    if (time.isBefore(past_limit)) {
        frappe.msgprint(__("You cannot select a date older than " + older_days + " Days in the past"));
        frappe.model.set_value(cdt, cdn, 'custom_date', null); 
        frappe.model.set_value(cdt, cdn, 'from_time', null);
        frappe.model.set_value(cdt, cdn, 'to_time', null);
        return; 
    }

    if (time.isAfter(future_limit)) {
        frappe.msgprint(__("You cannot select a date more than " + future_days + " Days in the future."));
        frappe.model.set_value(cdt, cdn, 'custom_date', null); 
        frappe.model.set_value(cdt, cdn, 'from_time', null);
        frappe.model.set_value(cdt, cdn, 'to_time', null);
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