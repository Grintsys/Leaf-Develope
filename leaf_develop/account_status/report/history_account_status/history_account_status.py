# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	data = []

	columns = [
		{
   			"fieldname": "movement_type",
  			"fieldtype": "Data",
  			"label": "Movement Type",
  		},
		{
			"fieldname": "date",
   			"fieldtype": "Data",
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
	
	req_data = [{'indent': 0.0, "movement_type": "Requisiciones"},
	{'indent': 1.0, "movement_type": "Requisicion1", "date": "23/12/2020"},
	{'indent': 2.0, "movement_type": "Requisicion1.1", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 1.0, "movement_type": "Requisicion2", "date": "23/12/2020"},
	{'indent': 2.0, "movement_type": "Requisicion2.1", "date": "23/12/2020", "item":"Loratadina", "quantity": "2"},
	{}
	]

	data.extend(req_data or [])

	req_data = [{'indent': 0.0, "movement_type": "Retorno de Requisiciones"},
	{'indent': 1.0, "movement_type": "Retorno Requisicion1", "date": "25/12/2020"},
	{'indent': 2.0, "movement_type": "Retorno Requisicion1.1", "date": "26/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 1.0, "movement_type": "Retorno Requisicion2", "date": "27/12/2020"},
	{'indent': 2.0, "movement_type": "Retotno Requisicion2.1", "date": "29/12/2020", "item":"Loratadina", "quantity": "2"},
	{}
	]

	data.extend(req_data or [])

	req_data = [{'indent': 0.0, "movement_type": "Honorarios Medicos"},
	{'indent': 1.0, "movement_type": "Honorarios Medicos1", "date": "25/12/2020"},
	{'indent': 2.0, "movement_type": "Honorarios Medicos1.1", "date": "26/12/2020", "item":"Loratadina", "quantity": "2"},
	{'indent': 1.0, "movement_type": "Honorarios Medicos2", "date": "27/12/2020"},
	{'indent': 2.0, "movement_type": "Honorarios Medicos2.1", "date": "29/12/2020", "item":"Loratadina", "quantity": "2"},
	]

	data.extend(req_data or [])

	return columns, data
