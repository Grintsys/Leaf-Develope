// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Payment Of Honorarium"] = {
	"filters": [
		{
			fieldname:"medical",
			label: __("Medical"),
			fieldtype: "Link",
			options: "Medical",
			reqd: 1,
			get_query: () => {
				return {
					filters: {
						"status": "Active"
					}
				}
			}
		},
		{
			fieldname:"patient_statement",
			label: __("Patient Statement"),
			fieldtype: "Link",
			options: "Patient statement",
			// get_query: () => {
			// 	return {
			// 		filters: {
			// 			"status": "Active"
			// 		}
			// 	}
			// }
		},
		{
			fieldname:"status",
			label: __("Status"),
			fieldtype: "Select",
			options:["Open", "Paid Out", "All"],
			default:"Paid Out"
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1
		}

	]
};
