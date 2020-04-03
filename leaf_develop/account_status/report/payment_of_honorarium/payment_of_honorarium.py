# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	columns = [
		_("Patient Statement") + "::180", _("Medical") + "::200", _("Honorarium") + "::180", _("Status") + "::119",
		_("Total") + ":Currency:140",  _("Total Payment") + ":Currency:140", _("Total Remaining") + ":Currency:140"
	]

	data = []

	conditions = return_filters(filters)

	honorarium = frappe.get_all("Medical Honorarium", ["name", "name_medical", "patient_statement", "total", "total_remaining", "status", "total_payment"], filters = conditions)

	for item in honorarium:
		row = [item.patient_statement, item.name_medical, item.name, item.status, item.total, item.total_payment, item.total_remaining]
		data.append(row)
	
	return columns, data

def return_filters(filters):
	conditions = ''

	conditions += "{"
	if filters.get("from_date") and filters.get("to_date"): conditions += '"date": [">=", "{}", "<=", "{}"], '.format(filters.get("from_date"), filters.get("to_date"))
	if filters.get("medical"): conditions += '"medical": "{}"'.format(filters.get("medical"))
	if filters.get("patient_statement"): conditions += ', "patient_statement": "{}"'.format(filters.get("patient_statement"))
	if filters.get("status") != "All":
		if filters.get("status"): conditions += ', "status": "{}"'.format(filters.get("status"))
	conditions += '}'

	return conditions

