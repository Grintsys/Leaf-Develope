// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laboratory And Image', {
	// refresh: function(frm) {

	// }
	onload: function (frm) {
		cur_frm.fields_dict['patient_statement'].get_query = function (doc, cdt, cdn) {
			return {
				filters: { 'state': ["=", "Open"], 'acc_sta': ["=", "Open"] }
			}
		}
	},

	setup: function (frm) {
		var category_for_sale_laboratory_and_image = "Vacio";

		frappe.db.get_list('Patient Warehouse', {
			fields: ['category_for_sale_laboratory_and_image'],
			order_by: 'creation asc'
		}).then(result => {
			console.log(result)
			category_for_sale_laboratory_and_image = result[0].category_for_sale_laboratory_and_image
		})

		frm.set_query("item", "products", function (doc, cdt, cdn) {
			return {
				filters: { "default_company": doc.company, "category_for_sale": category_for_sale_laboratory_and_image }
			};
		});
	},
});
