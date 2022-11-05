# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = [
		{
   			"fieldname": "patient_statement",
  			"fieldtype": "Data",
  			"label": "Patient Statement",
  		},
		{
			"fieldname": "medical",
   			"fieldtype": "Data",
   			"label": "Medical"
		},
		{
   			"fieldname": "medical_honorarium",
  			"fieldtype": "Link",
  			"label": "Honorarium",
			"options": "Medical Honorarium"
  		},
		{
			"fieldname": "status",
   			"fieldtype": "Data",
   			"label": "Status"
		},
		{
			"fieldname": "total",
   			"fieldtype": "Currency",
   			"label": "Price"
		},
		{
			"fieldname": "total_payment",
   			"fieldtype": "Currency",
   			"label": "Total Payment"
		},
		{
			"fieldname": "total_remaining",
   			"fieldtype": "Currency",
   			"label": "Total Remaining"
		}
	]
	
	data = []
	if filters.get("from_date"): from_date = filters.get("from_date")
	if filters.get("to_date"): to_date = filters.get("to_date")
	conditions = return_filters(filters, from_date, to_date)

	honorarium = frappe.get_all("Medical Honorarium", ["name", "name_medical", "patient_statement", "total", "total_remaining", "status", "total_payment"], filters = conditions)

	for item in honorarium:
		row = [item.patient_statement, item.name_medical, item.name, item.status, item.total, item.total_payment, item.total_remaining]
		data.append(row)
	
	return columns, data

def return_filters(filters, from_date, to_date):
	conditions = ''

	conditions += "{"
	conditions += '"date": ["between", ["{}", "{}"]]'.format(from_date, to_date)
	if filters.get("medical"): conditions += ', "medical": "{}"'.format(filters.get("medical"))
	if filters.get("patient_statement"): conditions += ', "patient_statement": "{}"'.format(filters.get("patient_statement"))
	if filters.get("status") != "All":
		if filters.get("status"): conditions += ', "status": "{}"'.format(filters.get("status"))
	conditions += '}'

	return conditions

