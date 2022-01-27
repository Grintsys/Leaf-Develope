# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	columns= [_("Date") + "::240", _("Patient Statement") + "::240", _("Item Code") + "::240", _("Item Name") + "::240", _("Type Transaction") + "::240", _("No Ttransaction") + "::240", _("Qty") + "::240"]
	data = return_data(filters)
	return columns, data

def return_data(filters):
	data = []

	if filters.get("from_date"): from_date = filters.get("from_date")
	if filters.get("to_date"): to_date = filters.get("to_date")

	conditions = return_filters_inventory_requisiton(filters, from_date, to_date)

	requisitions = frappe.get_all("Inventory Requisition", ["*"], filters = conditions)

	for requisition in requisitions:
		items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": requisition.name})

		for item in items:
			row = [requisition.date_create, requisition.patient_statement, item.item, item.product_name, "Requisición de inventario", requisition.name, item.quantity]
			data.append(row)
	
	conditions = return_filters_inventory_requisiton(filters, from_date, to_date)

	requisitions_return = frappe.get_all("Return of inventory requisition", ["*"], filters = conditions)

	for requisition in requisitions_return:
		items = frappe.get_all("Inventory Item Return", ["*"], filters = {"parent": requisition.name})

		for item in items:
			row = [requisition.date_create, requisition.patient_statement, item.item, item.product_name, "Retorno de requisición de inventario", requisition.name, item.quantity]
			data.append(row)

	return data

def return_filters_inventory_requisiton(filters, from_date, to_date):
	conditions = ''	

	conditions += "{"
	conditions += '"date_create": ["between", ["{}", "{}"]]'.format(from_date, to_date)
	if filters.get("patient_statement"): conditions += ', "patient_statement": "{}"'.format(filters.get("patient_statement"))
	conditions += '}'

	return conditions
