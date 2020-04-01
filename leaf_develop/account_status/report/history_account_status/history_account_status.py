# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	data = []

	columns = [
		{
   			"fieldname": "item",
  			"fieldtype": "Data",
  			"label": "Product",
  		},
		{
			"fieldname": "date",
   			"fieldtype": "Data",
   			"label": "Date"
		},
		{
			"fieldname": "date",
   			"fieldtype": "Datetime",
   			"label": "Date"
		},
		{
   			"fieldname": "item",
  			"fieldtype": "Data",
  			"label": "Product",
  		},
		{
   			"fieldname": "quantity",
   			"fieldtype": "Data",
   			"label": "Quantity",
  		}
	]
	req_data = [{'indent': 0.0, "Movement Type": "Requisicion", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 1.0, "Movement Type": "Requisicion1", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 2.0, "Movement Type": "Requisicion1.1", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 1.0, "Movement Type": "Requisicion2", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 2.0, "Movement Type": "Requisicion2.1", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	]

	data.extend(req_data or [])

	frappe.msgprint("data {}".format(data))
	frappe.msgprint("columns {}".format(columns))

	return columns, data
