from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
			"label": _("Account Status"),
			"items": [
				{
					"type": "doctype",
					"name": "Patient statement",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Advance Statement",
					"onboard": 1,
					"dependencies": ["Patient statement"]
				},
				{
					"type": "doctype",
					"name": "Return Advance Statement",
					"onboard": 1,
					"dependencies": ["Patient statement"]
				},
				{
					"type": "doctype",
					"name": "Inventory Requisition",
					"onboard": 1,
					"dependencies": ["Patient statement"]
				},
				{
					"type": "doctype",
					"name": "Return of inventory requisition",
					"onboard": 1,
					"dependencies": ["Inventory Requisition"]
				},
                {
                    "type": "doctype",
                    "name": "Medical Honorarium",
                    "onboard": 1,
                }
			]
		},
        {
            "label": _("Doctors"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Medical",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Specialty",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Honorarium Payment",
                    "onboard": 1,
                }
            ]
        },
        {
            "label": _("Reports"),
            "items": [
                {
					"type": "report",
					"is_query_report": True,
					"name": "Payment Of Honorarium",
					"doctype": "Payment Of Honorarium",
                    "dependencies": ["Medical Honorarium"]
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "Patient Medical Fees",
					"doctype": "Patient Medical Fees",
                    "dependencies": ["Medical Honorarium"]
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "History Account Status",
					"doctype": "History Account Status",
                    "dependencies": ["Medical Honorarium", "Return of inventory requisition", "Inventory Requisition"]
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "General report of hospital accounts",
					"doctype": "General report of hospital accounts",
                    "dependencies": ["Patient statement"]
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Detailed general report of hospital accounts",
					"doctype": "Detailed general report of hospital accountss",
                    "dependencies": ["Patient statement"]
				}
            ]
        }
    ]
