// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Advance Statement', {
	// refresh: function(frm) {

	// }

	onload: function(frm) {
		cur_frm.fields_dict['patient_statement'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'outstanding_balance': [">",0]}
			}
		}
	}
});
