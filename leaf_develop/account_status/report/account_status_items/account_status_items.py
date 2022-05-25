# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	columns = [
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 240
		},
		{
			"label": _("Patient Statement"),
			"fieldname": "patient_statement",
			"width": 240
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 240
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"width": 240
		},
		{
			"label": _("Type Transaction"),
			"fieldname": "voucher_type",
			"width": 240
		},
		{
			"label": _("No Transaction"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 240
		},
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"width": 120
		}
	]
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
			row = [requisition.date_create, requisition.patient_statement, item.item, item.product_name, "Inventory Requisition", requisition.name, item.quantity]
			data.append(row)
		
		condition_entry = return_filters_stock_entry(filters, from_date, to_date, requisition.name)

		entries = frappe.get_all("Stock Entry", ["*"], filters = condition_entry)

		for entry in entries:
			items_entry = frappe.get_all("Stock Entry Detail", ["*"], filters = {"parent": entry.name})

			for item_entry in items_entry:
				row = [entry.posting_date, requisition.patient_statement, item_entry.item_code, item_entry.item_name, "Stock Entry", entry.name, item_entry.qty]
				data.append(row)
	
	conditions = return_filters_inventory_requisiton(filters, from_date, to_date)

	requisitions_return = frappe.get_all("Return of inventory requisition", ["*"], filters = conditions)

	for requisition in requisitions_return:
		items = frappe.get_all("Inventory Item Return", ["*"], filters = {"parent": requisition.name})

		for item in items:
			row = [requisition.date_create, requisition.patient_statement, item.item, item.product_name, "Return of inventory requisition", requisition.name, item.quantity]
			data.append(row)
	

	return data

def return_filters_inventory_requisiton(filters, from_date, to_date):
	conditions = ''	

	conditions += "{"
	conditions += '"date_create": ["between", ["{}", "{}"]]'.format(from_date, to_date)
	if filters.get("patient_statement"): conditions += ', "patient_statement": "{}"'.format(filters.get("patient_statement"))
	conditions += '}'

	return conditions

def return_filters_stock_entry(filters, from_date, to_date, requisition):
	conditions = ''	

	conditions += "{"
	conditions += '"inventory_requisition": "{}"'.format(requisition)
	conditions += '}'

	return conditions
