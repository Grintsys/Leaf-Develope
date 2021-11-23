# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	columns= [_("Serie") + "::240", _("Status") + "::240", _("Date") + "::240", _("Patient Statement") + "::240", _("Patient Name") + "::240", _("Cashier") + "::240", _("Way to pay") + "::240", _("amount") + ":Currency:120"]
	data = return_data(filters)
	return columns, data

def return_data(filters):
	data = []

	if filters.get("from_date"): from_date = filters.get("from_date")
	if filters.get("to_date"): to_date = filters.get("to_date")
	conditions = return_filters(filters, from_date, to_date)

	advances = frappe.get_all("Advance Statement", ["*"], filters = conditions)

	if len(advances):
		for advance in advances:
			row = [advance.name, advance.state, advance.date_create, advance.patient_statement, advance.patient_name, advance.cashier, advance.way_to_pay, advance.amount]
			data.append(row)
	
	return data

def return_filters(filters, from_date, to_date):
	conditions = ''	

	conditions += "{"
	conditions += '"date_create": ["between", ["{}", "{}"]]'.format(from_date, to_date)
	if filters.get("patient_statement"):
		conditions += ', "patient_statement": "{}"'.format(filters.get("patient_statement"))
	conditions += '}'

	return conditions
