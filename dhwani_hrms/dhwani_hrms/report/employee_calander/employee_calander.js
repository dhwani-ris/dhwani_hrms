frappe.query_reports["Employee Calander"] = {
	"filters": [
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: [
				"January", "February", "March", "April", "May", "June",
				"July", "August", "September", "October", "November", "December"
			],
			default: moment().format('MMMM') 
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Select",
			options: [moment().subtract(1, 'year').format('YYYY'), moment().format('YYYY'), moment().add(1, 'year').format('YYYY')], // Example years
			default: moment().format('YYYY')
		},
		{
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
        },
	],
	"formatter": function(value, row, column, data, default_formatter) {
        if (column.fieldname === "employee" || column.fieldname === "employee_name") {
            return `<span style='color:black !important;'>${default_formatter(value, row, column, data)}</span>`; 
        } else if (typeof value === 'string') {
            let color;

            switch (value) {
                case "Present":
                    color = "green";
                    break;
                case "Absent":
                    color = "red";
                    break;
                case "Leave":
                    color = "orange";
                    break;
                case "Work From Home":
                    color = "purple";
                    break;
                case "Weekoff":
                    color = "gray";
                    break;
                default:
                    if (value && value.includes("Leave")) {
                        color = "orange";
                    } else if (value && value.includes("Work From Home")) {
                        color = "purple";
                    } else if (value && value.includes("Present")) {
                        color = "green";
                    } else {
                        color = "gray"; 
                    }
            }

            if (color) {
                return `<span style='color:${color}!important'>${value}</span>`;
            }
        }

        return default_formatter(value, row, column, data); 
    }
};
