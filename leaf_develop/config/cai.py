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
              "name": "GCAI",
              "label": _("GCAI"),
              "description": _("This option is for create new cais."),
	      "hide_count": True,
	      "onboard": 1,
	      "dependencies": ["GType Document", "GSucursal", "GPos", "GNumber Declaration"]
            },
	    {
              "type": "doctype",
              "name": "GCAI Allocation",
              "label": _("GCAI Allocation"),
              "description": _("This option is assign cai to users."),
	      "hide_count": True,
	      "onboard": 1,
	      "dependencies": ["GCAI"]
            }
          ]
        },
        {
	    "label": _("Maintenance"),
	    "items":[
	        {
              "type": "doctype",
              "name": "GType Document",
              "label": _("GType Document"),
	      "onboard": 1,
              "description": _("This doctype is for create new documents types.")
            },
	        {
              "type": "doctype",
              "name": "GSucursal",
              "label": _("GSucursal"),
              "description": _("This doctype is for create new sucursales."),
	          "onboard": 1
            },
	        {
              "type": "doctype",
              "name": "GPos",
              "label": _("GPos"),
              "description": _("This doctype is for create new Pos."),
	          "hide_count": True,
	          "onboard": 1,
	          "dependencies": ["GSucursal"]
            },
	        {
              "type": "doctype",
              "name": "GNumber Declaration",
              "label": _("GNumber Declaration"),
              "description": _("This doctype is for create new number declaration."),
	          "onboard": 1
            }
	    ]
    },
    {
        "label":_("Settings"),
        "items": [
            {
              "type": "doctype",
              "name": "GCai Settings",
              "label": _("GCai Settings"),
              "description": _("This doctype is for update of settings."),
	          "onboard": 1
            }
        ]
    }
  ]
