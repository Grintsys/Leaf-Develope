# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _, msgprint

def execute(filters=None):
	if not filters: filters = {}
	columns = [
		_("Patient Statement") + "::180", _("Customer") + "::200", _("Honorarium") + "::180", _("Status") + "::119",
		_("Total") + ":Currency:140",  _("Total Payment") + ":Currency:140", _("Total Remaining") + ":Currency:140"
	]

	data = []

	conditions = return_filters(filters)
	honorarium = frappe.get_all("Medical Honorarium", ["name", "name_medical", "patient_statement", "total", "total_remaining", "status", "total_payment"], filters = conditions)
	for item in honorarium:
		conditions_patient = return_patient(filters, item.patient_statement)
		patient_statement = frappe.get_all("Patient statement", ["name", "client"], filters = conditions_patient)
		for patient in patient_statement:
			row = [item.patient_statement, patient.client, item.name, item.status, item.total, item.total_payment, item.total_remaining]
			data.append(row)
	
	return columns, data

def return_filters(filters):
	conditions = ''

	conditions += "{"
	if filters.get("status") != "All": conditions += '"status": "{}", '.format(filters.get("status"))
	if filters.get("patient_statement"): conditions += '"patient_statement": "{}", '.format(filters.get("patient_statement"))
	if filters.get("from_date") and filters.get("to_date"): conditions += '"date": [">=", "{}"], "date": ["<=", "{}"]'.format(filters.get("from_date"), filters.get("to_date"))
	conditions += "}"

	return conditions

def return_patient(filters, patient_statement):
	conditions = ''

	conditions += "{"
	conditions += '"name": "{}"'.format(patient_statement)
	if filters.get("customer"): conditions += ', "client": "{}"'.format(filters.get("customer"))
	conditions += '}'

	return conditions
