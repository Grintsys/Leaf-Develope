// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Detailed general report of hospital accounts"] = {
	"filters": [
		{
			"fieldname":"patient_statement",
			"label": __("Patient Statement"),
			"fieldtype": "Link",
			"options": "Patient statement",
			"reqd": 1
		},
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default":"Submitted"
		}
	]
};
