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
            }
          ]
        }
  ]
