from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
      {
        "label":_("CAI"),
        "icon": "octicon octicon-book",
        "items": [
            {
              "type": "doctype",
              "name": "CAI",
              "label": _("CAI"),
              "description": _("This option is for create new cais."),
	      "hide_count": True,
	      "onboard": 1
            },
            {
              "type": "doctype",
              "name": "Naming Series",
              "label": _("Naming Series"),
              "description": _("Create secuences."),
	      "hide_count": True,
	      "onboard": 1
            },
            {
              "type": "doctype",
              "name": "Cai Settings",
              "label": _("Cai Settings"),
              "description": _("This option is for create new settings"),
	      "hide_count": True,
	      "onboard": 1
            },
          ]
        }
  ]
