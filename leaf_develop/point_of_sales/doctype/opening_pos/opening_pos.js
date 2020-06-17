// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Opening POS', {

	after_save: function(frm) {
		frappe.set_route("point-of-sales")
	}
});
