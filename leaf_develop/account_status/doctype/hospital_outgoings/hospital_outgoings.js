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
		var category_for_sale_hospital_outgoings = "Vacio";
		var category_for_sale_procedure = "Vacio";

		frappe.db.get_list('Patient Warehouse', {
			fields: ['category_for_sale_hospital_outgoings', 'category_for_sale_procedure'],
			order_by: 'creation asc'
		}).then(result => {
			console.log(result)
			category_for_sale_hospital_outgoings = result[0].category_for_sale_hospital_outgoings
			category_for_sale_procedure = result[0].category_for_sale_procedure
		})

		frm.set_query("item", "products", function(doc, cdt, cdn) {
			if (doc.type === "Procedures"){
				return {
					filters:{"default_company": doc.company, "category_for_sale": category_for_sale_procedure}
				};
			}	

			if (doc.type === "Hospital Outgoing"){
				return {
					filters:{"default_company": doc.company, "category_for_sale": category_for_sale_hospital_outgoings}
				};
			}
		});
    },
});
