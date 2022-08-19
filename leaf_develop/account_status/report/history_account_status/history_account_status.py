# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	data = []

	columns = [
		{
   			"fieldname": "movement_type",
  			"fieldtype": "Data",
  			"label": "Movement Type",
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
   			"label": "Quantity",
  		}
	]

	arr_requisition = []
	arr_return = []
	arr_honorarium = []
	arr_gastos = []
	arr_laboratory = []

	conditions = get_conditions(filters)
	
	req_data = [{'indent': 0.0, "movement_type": "Requisiciones"}]

	requisitions = frappe.get_all("Inventory Requisition", ["name", "date_create"], filters = conditions, order_by = "date_create asc")

	for requisition in requisitions:
		if str(requisition.date_create) >= str(filters.get("from_date")) and str(requisition.date_create) <= str(filters.get("to_date")):
			req_data += [{'indent': 1.0, "movement_type": requisition.name, "date": requisition.date_create}]
			arr_requisition += [requisition.date_create]
			
			inventory_items = frappe.get_all("Inventory Item", ["product_name", "quantity"], filters = {"parent": requisition.name})

			for inventory_item in inventory_items:
				req_data += [{'indent': 2.0, "movement_type": requisition.name, "date": requisition.date_create, "item":inventory_item.product_name, "quantity": inventory_item.quantity}]

	req_data += [{}]

	req_data += [{'indent': 0.0, "movement_type": "Retorno de Requisiciones"}]

	return_requisitions = frappe.get_all("Return of inventory requisition", ["name", "date_create"], filters = conditions, order_by = "date_create asc")

	for return_requisition in return_requisitions:
		if str(return_requisition.date_create) >= str(filters.get("from_date")) and str(return_requisition.date_create) <= str(filters.get("to_date")):
			req_data += [{'indent': 1.0, "movement_type": return_requisition.name, "date": return_requisition.date_create}]
			arr_return += [return_requisition.date_create]

			inventory_items_return = frappe.get_all("Inventory Item Return", ["product_name", "quantity"], filters = {"parent": return_requisition.name})

			for inventory_item_return in inventory_items_return:
				req_data += [{'indent': 2.0, "movement_type": return_requisition.name, "date": return_requisition.date_create, "item":inventory_item_return.product_name, "quantity": inventory_item_return.quantity}]
	
	req_data += [{}]

	req_data += [{'indent': 0.0, "movement_type": "Gastos Hospitalarios"}]	

	condition_gastos = get_conditions_hospital_expenses(filters)
	
	gastos = frappe.get_all("Hospital Expenses", ["name", "creation_date", "product_name"], filters = condition_gastos, order_by = "creation_date asc")

	for gasto in gastos:
		gastos_detail = frappe.get_all("Hospital Expenses Detail", ["name"], filters = {"parent": gasto.name})
		req_data += [{'indent': 1.0, "movement_type": gasto.name, "date": gasto.creation_date, "item": gasto.product_name, "quantity": len(gastos_detail)}]
		arr_gastos += [gasto.creation_date]
	
	hospital_outgoings = frappe.get_all("Hospital Outgoings", ["name", "date_create"], filters = conditions, order_by = "date_create asc")

	for requisition in hospital_outgoings:
		if str(requisition.date_create) >= str(filters.get("from_date")) and str(requisition.date_create) <= str(filters.get("to_date")):
			# req_data += [{'indent': 1.0, "movement_type": requisition.name, "date": requisition.date_create}]
			arr_requisition += [requisition.date_create]
			
			inventory_items = frappe.get_all("Inventory Item", ["product_name", "quantity"], filters = {"parent": requisition.name})

			for inventory_item in inventory_items:
				req_data += [{'indent': 1.0, "movement_type": requisition.name, "date": requisition.date_create, "item":inventory_item.product_name, "quantity": inventory_item.quantity}]
				arr_gastos += [requisition.date_create]
	
	req_data += [{}]

	req_data += [{'indent': 0.0, "movement_type": "Gastos de laboratorio"}]	

	condition_gastos = get_conditions_laboratory_expenses(filters)
	
	laboratories = frappe.get_all("Laboratory Expenses", ["name", "creation_date", "product_name", "total_amount"], filters = condition_gastos, order_by = "creation_date asc")
	
	for laboratory in laboratories:
		req_data += [{'indent': 1.0, "movement_type": laboratory.name, "date": laboratory.creation_date, "item": laboratory.product_name, "quantity": 1}]
		arr_laboratory += [laboratory.creation_date]
	
	lab_img = frappe.get_all("Laboratory And Image", ["name", "date_create"], filters = conditions, order_by = "date_create asc")

	for requisition in lab_img:
		if str(requisition.date_create) >= str(filters.get("from_date")) and str(requisition.date_create) <= str(filters.get("to_date")):
			# req_data += [{'indent': 1.0, "movement_type": requisition.name, "date": requisition.date_create}]
			arr_requisition += [requisition.date_create]
			
			inventory_items = frappe.get_all("Inventory Item", ["product_name", "quantity"], filters = {"parent": requisition.name})

			for inventory_item in inventory_items:
				req_data += [{'indent': 1.0, "movement_type": requisition.name, "date": requisition.date_create, "item":inventory_item.product_name, "quantity": inventory_item.quantity}]
				arr_laboratory += [requisition.date_create]

	req_data += [{}]

	req_data += [{'indent': 0.0, "movement_type": "Honorarios Medicos"}]

	condition_honorarium = get_conditions_honorarium(filters)

	honorariums = frappe.get_all("Medical Honorarium", ["name", "date", "medical"], filters = condition_honorarium, order_by = "date asc")

	for honorarium in honorariums:
		if str(honorarium.date) >= str(filters.get("from_date")) and str(honorarium.date) <= str(filters.get("to_date")):
			medico = frappe.get_all("Medical", ["service"], filters = {'name': honorarium.medical})

			for med in medico:
				products = frappe.get_all("Item", ["item_name"], filters = {'name': med.service})

				for product in products:
					req_data += [{'indent': 1.0, "movement_type": honorarium.name, "date": honorarium.date, "item": product.item_name, "quantity": 1}]
					arr_honorarium += [honorarium.date]

	data.extend(req_data or [])

	message = None

	# labels = []

	# labels = get_labels(labels, arr_requisition)
	# labels = get_labels(labels, arr_return)
	# labels = get_labels(labels, arr_honorarium)	

	# values_data = []

	# values_data_requisition = get_data_values(arr_requisition)	
	# values_data_return = get_data_values(arr_return)	
	# values_data_honorarium = get_data_values(arr_honorarium)

	# if len(values_data_requisition) > len(values_data_return) and len(values_data_requisition) > len(values_data_honorarium):
	# 	values_data_return = add_values(values_data_requisition, values_data_return)
	# 	values_data_honorarium = add_values(values_data_requisition, values_data_honorarium)
	
	# if len(values_data_return) > len(values_data_requisition) and len(values_data_return) > len(values_data_honorarium):
	# 	values_data_requisition = add_values(values_data_return, values_data_requisition)
	# 	values_data_honorarium = add_values(values_data_return, values_data_honorarium)
	
	# if len(values_data_honorarium) > len(values_data_requisition) and len(values_data_honorarium) > len(values_data_return):
	# 	values_data_requisition = add_values(values_data_honorarium, values_data_requisition)
	# 	values_data_return = add_values(values_data_honorarium, values_data_return)

	# datasets = []
	
	# datasets = get_dataset(datasets, values_data_requisition, "Requisiciones")
	# datasets = get_dataset(datasets, values_data_return, "Retorno de requisiciones")
	# datasets = get_dataset(datasets, values_data_honorarium, "Honorarios Medicos")

	labels = ["Requisiciones", "Retorno de requisiciones", "Gastos Hospitalarios", "Gastos De Laboratorio", "Honorarios Medicos"]
	datasets = []

	datasets += [{'values': [len(arr_requisition), len(arr_return),len(arr_gastos), len(arr_laboratory), len(arr_honorarium)]}]

	chart= {
		'data': 
		{
			'labels': labels, 
			'datasets': datasets
		}, 
		'type': 'bar'
	}

	return columns, data, message, chart

def get_conditions(filters):
	conditions = ''

	conditions += "{"
	if filters.get("from_date") and filters.get("to_date"): conditions += '"date_create": [">=", "{}", "<=", "{}"], "docstatus": 1'.format(filters.get("from_date"), filters.get("to_date"))
	conditions += "}"

	return conditions

def get_conditions_honorarium(filters):
	conditions = ''

	conditions += "{"
	if filters.get("from_date") and filters.get("to_date"): conditions += '"date": [">=", "{}", "<=", "{}"]'.format(filters.get("from_date"), filters.get("to_date"))
	conditions += "}"

	return conditions

def get_conditions_hospital_expenses(filters):
	conditions = ''

	conditions += "{"
	if filters.get("from_date") and filters.get("to_date"): conditions += '"creation_date": ["between", ["{}", "{}"]], "docstatus": 1'.format(filters.get("from_date"), filters.get("to_date"))
	conditions += "}"

	return conditions

def get_conditions_laboratory_expenses(filters):
	conditions = ''

	conditions += "{"
	if filters.get("from_date") and filters.get("to_date"): conditions += '"creation_date": ["between", ["{}", "{}"]], "docstatus": 1'.format(filters.get("from_date"), filters.get("to_date"))
	conditions += "}"

	return conditions

# def get_labels(labels, array):

# 	for arr in array:

# 		if len(labels) > 0:
# 			cont = 0
# 			for l in labels:
# 				cont += 1

# 				if l == arr:
# 					break

# 				if len(labels) == cont:
# 					labels.append(arr)
# 		else:
# 			labels.append(arr)
	
# 	return labels

# def get_data_values(array):
# 	values_data = []

# 	for arr in array:

# 		if len(values_data) > 0:
# 			cont = 0
# 			for value in values_data:
# 				cont += 1 

# 				if arr == value[1]:
# 					value[0] += 1
# 					break
				
# 				if len(values_data) == cont:
# 					values_data.append([1, arr])
# 					break
# 		else:
# 			values_data.append([1, arr])
	
# 	return values_data

# def get_dataset(datasets, array, name):
# 	values = []
	
# 	for arr in array:
# 		values.append(arr[0])
	
# 	datasets += [{'values': values, 'name': name}]

# 	return datasets

# def add_values(arr_max, arr_min):

# 	arr_return = []

# 	for arr in arr_max:
# 		cont = 0
# 		if len(arr_min) > 0:
# 			for arr_mi in arr_min:
# 				cont += 1
# 				if arr[1] == arr_mi[1]:
# 					arr_return.append([arr_mi[0], arr_mi[1]])
# 					break

# 				if cont == len(arr_min):
# 					arr_return.append([0, arr[1]])
# 					break
# 		else:
# 			arr_return.append([0, arr[1]])
# 			break
	
# 	return arr_return