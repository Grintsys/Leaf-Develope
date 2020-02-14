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
				}
			]
		}
    ]
