from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on the Time Sheets created against this project'),
		'fieldname': 'patient_statement',
		'transactions': [
			{
				'label': _('History'),
				'items': ['Inventory Requisition', 'Return of inventory requisition', 'Hospital Outgoings', 'Laboratory And Image', 'Advance Statement', 'Medical Honorarium', 'Account Statement Payment', 'Sales Invoice']
			},
        ]
	}
