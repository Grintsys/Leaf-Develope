// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient statement', {
	onload: function(frm) {
		frm.events.get_prefix(frm);
	},

	get_prefix: function(frm) {
		frappe.call({
			method: "get_prefix",
			doc: frm.doc,
			callback: function(r) {
				frm.set_df_property("naming_series", "options", r.message.prefix);
			}
		});
	},
});
