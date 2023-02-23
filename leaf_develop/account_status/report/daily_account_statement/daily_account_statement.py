# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
	if not filters: filters = {}
	
	columns = [
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Datetime",
		},
		{
			"label": _("Voucher Type"),
			"fieldname": "voucher_type",
			"width": 120
		},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180
		},
		{
			"fieldname": "item",
			"label": _("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 120
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "qty",
			"label": _("Quantity"),
			"fieldtype": "Int"
		},
		{
			"fieldname": "amount",
			"label": _("Amount"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		}
	]
	
	data = return_data(filters)
	return columns, data


def return_data(filters):
	data = []
	if filters.get("from_date"): from_date = filters.get("from_date")
	if filters.get("to_date"): to_date = filters.get("to_date")
	conditions = return_filters(filters, from_date, to_date)

	results = frappe.get_all("Inventory Requisition", ["*"], filters = conditions)

	for result in results:
		if verificate_hours(filters, result.date_create):
			items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": result.name})
			for item in items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": filters.get("patient_statement")})
				price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})

				totalPrice = 0

				if len(price) > 0:
					totalPrice = price[0].price

				row = [result.date_create, "Inventory Requisition", result.name, item.item, item.product_name, item.quantity, totalPrice]
				data.append(row)

	results = frappe.get_all("Hospital Outgoings", ["*"], filters = conditions)

	for result in results:
		if verificate_hours(filters, result.date_create):
			items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": result.name})
			for item in items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": filters.get("patient_statement")})
				price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})

				totalPrice = 0

				if len(price) > 0:
					totalPrice = price[0].price

				row = [result.date_create, "Hospital Outgoings", result.name, item.item, item.product_name, item.quantity, totalPrice]
				data.append(row)

	results = frappe.get_all("Laboratory And Image", ["*"], filters = conditions)

	for result in results:
		if verificate_hours(filters, result.date_create):
			items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": result.name})
			for item in items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": filters.get("patient_statement")})
				price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})

				totalPrice = 0

				if len(price) > 0:
					totalPrice = price[0].price
									
				row = [result.date_create, "Laboratory And Image", result.name, item.item, item.product_name, item.quantity, totalPrice]
				data.append(row)
	
	conditions = return_filters_medical_honorarium(filters)
	
	honorariums = frappe.get_all("Medical Honorarium", ["*"], filters = conditions)

	for honorarium in honorariums:
		items = frappe.get_all("Medical Honorarium Detail", ["*"], filters = {"parent": honorarium.name, "date": ["between", [from_date, to_date]]})

		for item in items:
			if verificate_hours(filters, item.date):
				medical = frappe.get_doc("Medical", honorarium.medical)
				itemValues = frappe.get_doc("Item", medical.service)
				row = [item.date, "Medical Honorarium", honorarium.name, medical.service, itemValues.item_name, 1, item.amount]
				data.append(row)
	
	conditions = return_filters(filters, from_date, to_date)
	
	results = frappe.get_all("Return of inventory requisition", ["*"], filters = conditions)

	for result in results:
		if verificate_hours(filters, result.date_create):
			items = frappe.get_all("Inventory Item Return", ["*"], filters = {"parent": result.name})
			for item in items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": filters.get("patient_statement")})
				price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})

				totalPrice = 0

				if len(price) > 0:
					totalPrice = price[0].price * -1

				row = [result.date_create, "Return of inventory requisition", result.name, item.item, item.product_name, item.quantity, totalPrice]
				data.append(row)
	
	results = frappe.get_all("Return Laboratory And Hospital Expenses", ["*"], filters = conditions)

	for result in results:
		if verificate_hours(filters, result.date_create):
			items = frappe.get_all("Inventory Item Return", ["*"], filters = {"parent": result.name})
			for item in items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": filters.get("patient_statement")})
				price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})

				totalPrice = 0

				if len(price) > 0:
					totalPrice = price[0].price * -1

				row = [result.date_create, "Return Laboratory And Hospital Expenses", result.name, item.item, item.product_name, item.quantity, totalPrice]
				data.append(row)

	return data

def verificate_hours(filters, date):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	is_valid = False

	date_str = date.strftime('%Y-%m-%d %H:%M:%S')

	if date_str >= from_date:
		if date_str <= to_date:
			is_valid = True
	
	return is_valid

def return_filters_medical_honorarium(filters):
	conditions = ''	

	conditions += "{"
	conditions += '"patient_statement": "{}"'.format(filters.get("patient_statement"))
	conditions += '}'

	return conditions

def return_filters(filters, from_date, to_date):
	conditions = ''	

	conditions += "{"
	conditions += '"date_create": ["between", ["{}", "{}"]]'.format(from_date, to_date)
	conditions += ', "patient_statement": "{}"'.format(filters.get("patient_statement"))
	conditions += ', "docstatus": 1'
	conditions += '}'

	return conditions
