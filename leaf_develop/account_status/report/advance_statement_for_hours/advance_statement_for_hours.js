// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Advance Statement For Hours"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"patient_statement",
			"label": __("Patient Statement"),
			"fieldtype": "Link",
			"options": "Patient statement",
			"reqd": 1
		}
	]
};
