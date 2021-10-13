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
			"fieldname": "date",
   			"fieldtype": "date",
   			"label": "Date"
		},
		{
   			"fieldname": "item",
  			"fieldtype": "Data",
  			"label": "Item",
  		},
		{
			"fieldname": "quantity",
   			"fieldtype": "Int",
   			"label": "Quantity"
		},
		{
			"fieldname": "total",
   			"fieldtype": "Currency",
   			"label": "Price"
		},
		{
			"fieldname": "total_price",
   			"fieldtype": "Currency",
   			"label": "TOTAL"
		}
	]
	data = []

	patientarr = []
	requisition = []
	return_requisition = []
	honorarium = []
	advance = []
	return_advance = []
	hospital_expense = []
	laboratory_expense = []

	arr_values = []
	condition = get_conditions(filters)

	requisition_detail = []
	return_requisition_detail = []
	honorarium_detail = []
	advance_detail = []
	return_advance_detail = []
	hospital_expense_detail = []
	laboratory_expense_detail = []
	
	patient_statement = frappe.get_all("Patient statement", ["name"], filters = condition)

	for patient in patient_statement:
		total_requisition = 0
		total_requisition_return = 0
		total_honorarium = 0
		total_advance = 0
		total_return_advance = 0
		total_gastos = 0
		total_laboratory = 0

		patientarr += [{'indent': 0.0, "movement": patient.name}]

		patient_requisition = frappe.get_all("Inventory Requisition", ["name", "date_create"], filters = {"patient_statement": patient.name, "docstatus": 1}, order_by = "date_create asc")

		for req in patient_requisition:
			requisition_detail += [{'indent': 2.0, "movement": req.name, "date": req.date_create}]
			inventory_items = frappe.get_all("Inventory Item", ["item", "product_name", "quantity"], filters = {"parent": req.name})

			for item in inventory_items:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": patient.name})

				price_acc_products = frappe.get_all("Account Statement Payment Item", ["price"], filters = {"parent": acc_sta[0].name, "item": item.item})

				if len(price_acc_products) > 0:
					price_total = item.quantity * price_acc_products[0].price
					total_requisition += price_total
					requisition_detail += [{'indent': 3.0, "movement": req.name, "date": req.date_create, "item": item.product_name, "quantity": item.quantity, "total": price_acc_products[0].price, "total_price": price_total}]
				else:
					price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item})
					price_total = item.quantity * price[0].price_list_rate
					total_requisition += price_total
					requisition_detail += [{'indent': 3.0, "movement": req.name, "date": req.date_create, "item": item.product_name, "quantity": item.quantity, "total": price[0].price_list_rate, "total_price": price_total}]

		requisition += [{'indent': 1.0, "movement": "Requisiciones", "quantity": len(patient_requisition), "total_price": total_requisition}]
		arr_values.append([len(patient_requisition), total_requisition])

		patient_return = frappe.get_all("Return of inventory requisition", ["name", "date_create"], filters = {"patient_statement": patient.name, "docstatus": 1}, order_by = "date_create asc")

		for ret in patient_return:
			return_requisition_detail += [{'indent': 2.0, "movement": ret.name, "date": ret.date_create}]
			inventory_items_return = frappe.get_all("Inventory Item Return", ["item", "product_name", "quantity"], filters = {"parent": ret.name})

			for item in inventory_items_return:
				acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": patient.name})

				price_acc_products = frappe.get_all("Account Statement Payment Item", ["price"], filters = {"parent": acc_sta[0].name, "item": item.item})
				
				if len(price_acc_products) > 0:
					price_total = item.quantity * price_acc_products[0].price
					total_requisition_return += price_total
					return_requisition_detail += [{'indent': 3.0, "movement": ret.name, "date": ret.date_create, "item": item.product_name, "quantity": item.quantity, "total": price_acc_products[0].price, "total_price": price_total}]
				else:
					price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item})
					price_total = item.quantity * price[0].price_list_rate
					total_requisition_return += price_total
					return_requisition_detail += [{'indent': 3.0, "movement": ret.name, "date": ret.date_create, "item": item.product_name, "quantity": item.quantity, "total": price[0].price_list_rate, "total_price": price_total}]

		return_requisition += [{}]
		return_requisition += [{'indent': 1.0, "movement": "Retorno de Requisiciones", "quantity": len(patient_return), "total_price": total_requisition_return}]
		arr_values.append([len(patient_return), total_requisition_return])

		honorariums = frappe.get_all("Medical Honorarium", ["name", "total", "date", "medical"], filters = {"patient_statement": patient.name}, order_by = "date asc")

		for hon in honorariums:
			total_honorarium += hon.total

			medico = frappe.get_all("Medical", ["service"], filters = {'name': hon.medical})

			for med in medico:
				products = frappe.get_all("Item", ["item_name"], filters = {'name': med.service})

				for product in products:
					honorarium_detail += [{'indent': 2.0, "movement": hon.name, "date": hon.date, "item": product.item_name, "quantity": 1, "total": hon.total, "total_price": hon.total}]
		
		honorarium += [{}]
		honorarium += [{'indent': 1.0, "movement": "Honorarios Medicos", "quantity": len(honorariums), "total_price": total_honorarium}]
		arr_values.append([len(honorariums), total_honorarium])
	
		gastos = frappe.get_all("Hospital Expenses", ["name", "creation_date", "product_name", "total_amount"], filters = {"patient_statement": patient.name, "docstatus": ["in", ["0", "1"]]}, order_by = "creation_date asc")

		for gasto in gastos:
			price_gasto =  0
			total_gastos +=  gasto.total_amount

			gastos_detail = frappe.get_all("Hospital Expenses Detail", ["name"], filters = {"parent": gasto.name})

			if gasto.total_amount > 0:
				price_gasto =  gasto.total_amount / len(gastos_detail)

			hospital_expense_detail += [{'indent': 2.0, "movement": gasto.name, "date": gasto.creation_date, "item": gasto.product_name, "quantity": len(gastos_detail), "total": price_gasto, "total_price": gasto.total_amount}]

		hospital_expense += [{}]
		hospital_expense += [{'indent': 1.0, "movement": "Gastos Hospitalarios", "quantity": len(gastos), "total_price": total_gastos}]
		arr_values.append([len(gastos), total_gastos])

		laboratories = frappe.get_all("Laboratory Expenses", ["name", "creation_date", "product_name", "total_amount"], filters = {"patient_statement": patient.name, "docstatus": ["in", ["0", "1"]]}, order_by = "creation_date asc")

		for laboratory in laboratories:
			price_laboratory =  0
			total_laboratory +=  laboratory.total_amount

			if gasto.total_amount > 0:
				price_laboratory =  laboratory.total_amount

			laboratory_expense_detail += [{'indent': 2.0, "movement": laboratory.name, "date": laboratory.creation_date, "item": laboratory.product_name, "quantity": len(gastos_detail), "total": price_laboratory, "total_price": laboratory.total_amount}]

		laboratory_expense += [{}]
		laboratory_expense += [{'indent': 1.0, "movement": "Gastos de laboratorio", "quantity": len(laboratories), "total_price": total_laboratory}]
		arr_values.append([len(laboratories), total_laboratory])

		advances = frappe.get_all("Advance Statement", ["name", "amount", "date_create"], filters = {"patient_statement": patient.name, "docstatus": 1}, order_by = "date_create asc")

		for adv in advances:
			total_advance -= adv.amount
			advamount = adv.amount - (adv.amount * 2)
			advance_detail += [{'indent': 2.0, "movement": adv.name, "date": adv.date_create, "quantity": 1, "total": advamount, "total_price": advamount}]
		
		advance += [{}]
		advance += [{'indent': 1.0, "movement": "Avances", "quantity": len(advances), "total_price": total_advance}]
		arr_values.append([len(advances), total_advance])

		return_advances = frappe.get_all("Return Advance Statement", ["name", "amount", "date_create"], filters = {"patient_statement": patient.name, "docstatus": 1}, order_by = "date_create asc")

		for radv in return_advances:
			total_return_advance += radv.amount
			return_advance_detail += [{'indent': 2.0, "movement": radv.name, "date": radv.date_create, "quantity": 1, "total": radv.amount, "total_price": radv.amount}]
		
		return_advance += [{}]
		return_advance += [{'indent': 1.0, "movement": "Retorno de avances", "quantity": len(return_advance_detail),"total_price": total_return_advance}]
		arr_values.append([len(return_advances), total_return_advance])

	data.extend(patientarr or [])
	data.extend(requisition or [])
	data.extend(requisition_detail or [])
	data.extend(return_requisition or [])
	data.extend(return_requisition_detail or [])
	data.extend(hospital_expense or [])
	data.extend(hospital_expense_detail or [])
	data.extend(laboratory_expense or [])
	data.extend(laboratory_expense_detail or [])
	data.extend(honorarium or [])
	data.extend(honorarium_detail or [])
	data.extend(advance or [])
	data.extend(advance_detail or [])
	data.extend(return_advance or [])
	data.extend(return_advance_detail or [])

	message = "Grafico por total"

	totales = []

	for val in arr_values:
		totales.append(val[1])

	labels = ["Requisiciones", "Retorno de requisciones", "Honorarios Medicos", "Avances", "Retorno de avances"]
	datasets = [{'values': totales}]

	chart= {
		'data': 
		{
			'labels': labels, 
			'datasets': datasets
		}, 
		'type': 'pie'
	}

	total_pen = totales[0] - totales[1] + totales[2] - totales[3] + totales[4]

	endtotal = [{'indent': 0.0, "movement": "Saldo Pendiente", "total_price": total_pen}]

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
