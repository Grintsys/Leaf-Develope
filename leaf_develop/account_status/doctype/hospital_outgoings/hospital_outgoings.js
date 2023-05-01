// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hospital Outgoings', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
		cur_frm.fields_dict['patient_statement'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'state': ["=","Open"], 'acc_sta': ["=","Open"]}
			}
		}
	},

	setup: function(frm) {
		frm.set_query("item", "products", function(doc, cdt, cdn) {
			if (doc.type === "Procedures"){
				return {
					filters:{"default_company": doc.company, "category_for_sale": "Procedimientos"}
				};
			}	

			if (doc.type === "Hospital Outgoing"){
				return {
					filters:{"default_company": doc.company, "category_for_sale": "Gastos Hospitalarios"}
				};
			}
		});
    },
});
