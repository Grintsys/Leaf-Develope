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
   			"fieldname": "movement",
  			"fieldtype": "Data",
  			"label": "Movement",
  		},
		{
			"fieldname": "quantity",
   			"fieldtype": "Int",
   			"label": "Quantity"
		},
		{
			"fieldname": "total",
   			"fieldtype": "Currency",
   			"label": "Total"
		}
	]
	data = []

	patientarr = []
	requisition = []
	return_requisition = []
	honorarium = []
	advance = []

	arr_values = []
	condition = get_conditions(filters)
	
	patient_statement = frappe.get_all("Patient statement", ["name"], filters = condition)

	for patient in patient_statement:
		total_requisition = 0
		total_requisition_return = 0
		total_honorarium = 0
		total_advance = 0

		patientarr += [{'indent': 0.0, "movement": patient.name}]

		patient_requisition = frappe.get_all("Inventory Requisition", ["name"], filters = {"patient_statement": patient.name, "docstatus": 1})

		for req in patient_requisition:
			inventory_items = frappe.get_all("Inventory Item", ["item", "product_name", "quantity"], filters = {"parent": req.name})

			for item in inventory_items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": patient.name})

				price_acc_products = frappe.get_all("Account Statement Payment Item", ["price"], filters = {"parent": acc_sta[0].name, "item": item.item})

				if len(price_acc_products) > 0:
					total_requisition += item.quantity * price_acc_products[0].price
				else:
					price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item})
					total_requisition += item.quantity * price[0].price_list_rate

		requisition += [{'indent': 1.0, "movement": "Requisiciones", "quantity": len(patient_requisition),"total": total_requisition}]
		arr_values.append([len(patient_requisition), total_requisition])

		patient_return = frappe.get_all("Return of inventory requisition", ["name"], filters = {"patient_statement": patient.name, "docstatus": 1})

		for ret in patient_return:
			inventory_items_return = frappe.get_all("Inventory Item Return", ["item", "product_name", "quantity"], filters = {"parent": ret.name})

			for item in inventory_items_return:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": patient.name})

				price_acc_products = frappe.get_all("Account Statement Payment Item", ["price"], filters = {"parent": acc_sta[0].name, "item": item.item})
				
				if len(price_acc_products) > 0:
					total_requisition_return += item.quantity * price_acc_products[0].price
				else:
					price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item})
					total_requisition_return += item.quantity * price[0].price_list_rate

		return_requisition += [{'indent': 1.0, "movement": "Retorno de Requisiciones", "quantity": len(patient_return),"total": total_requisition_return}]
		arr_values.append([len(patient_return), total_requisition_return])

		honorariums = frappe.get_all("Medical Honorarium", ["total"], filters = {"patient_statement": patient.name})

		for hon in honorariums:
			total_honorarium += hon.total
		
		honorarium += [{'indent': 1.0, "movement": "Honorarios Medicos", "quantity": len(honorariums),"total": total_honorarium}]
		arr_values.append([len(honorariums), total_honorarium])

		advances = frappe.get_all("Advance Statement", ["amount"], filters = {"patient_statement": patient.name, "docstatus": 1})

		for adv in advances:
			total_advance += adv.amount
		
		advance += [{'indent': 1.0, "movement": "Avances", "quantity": len(advances),"total": total_advance}]
		arr_values.append([len(advances), total_advance])

	data.extend(patientarr or [])
	data.extend(requisition or [])
	data.extend(return_requisition or [])
	data.extend(honorarium or [])
	data.extend(advance or [])

	message = "Grafico por total"

	totales = []

	for val in arr_values:
		totales.append(val[1])

	labels = ["Requisiciones", "Retorno de requisciones", "Honorarios Medicos", "Avances"]
	datasets = [{'values': totales}]

	chart= {
		'data': 
		{
			'labels': labels, 
			'datasets': datasets
		}, 
		'type': 'pie'
	}

	total_pen = totales[0] - totales[1] + totales[2] - totales[3]

	endtotal = [{'indent': 0.0, "movement": "Saldo Pendiente", "total": total_pen}]

	data.extend(endtotal)
	
	return columns, data, message, chart

def get_conditions(filters):
	conditions = ''
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	conditions += "{"
	if filters.get("docstatus"):
		conditions += '"docstatus": {0}, '.format(doc_status[filters.get("docstatus")])

	if filters.get("patient_statement"): conditions += '"name": "{}"'.format(filters.get("patient_statement"))
	conditions += "}"

	return conditions