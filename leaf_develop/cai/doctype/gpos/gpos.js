// Copyright (c) 2019, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('GPos', {
	// refresh: function(frm) {

	// }

	onload: function(frm) {
		cur_frm.fields_dict['sucursal'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'company': doc.company}
			}
		}
	}
});
