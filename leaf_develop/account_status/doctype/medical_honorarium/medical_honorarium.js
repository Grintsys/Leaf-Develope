// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Medical Honorarium', {
    onload: function (frm) {
        cur_frm.fields_dict['patient_statement'].get_query = function (doc, cdt, cdn) {
            return {
                filters: { 'state': "Open", 'acc_sta': ["=","Open"]}
            }
        }
    },
    
    setup: function (frm) {
        frm.set_query("medical", function () {
            return {
                "filters": {
                    "status": "Active"
                }
            }
        });
    }
});

