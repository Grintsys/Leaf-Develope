// Copyright (c) 2019, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('GCAI Allocation', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
		cur_frm.fields_dict['pos'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'sucursal': doc.branch}
			}
		}	
	}
});
