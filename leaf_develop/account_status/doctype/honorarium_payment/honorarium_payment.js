// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Honorarium Payment', {
	setup: function (frm) {
		frm.set_query("honorarium", function () {
			return {
				"filters": {
					"status": "Open"
				}
			}
		});
	}
});
