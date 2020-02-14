// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Medical Honorarium', {
    setup: function(frm) {
        frm.set_query("medical", function() {
            return{
                "filters": {
                    "docstatus": 1
                }
            }
        });
        }
});

