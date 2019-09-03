// Copyright (c) 2019, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('GCAI', {
	// refresh: function(frm) {

	//}

	// frappe.call({
	// 	method: 'frappe.client.get_list',
	// 	args: {
	// 		'doctype': 'GPos',
	// 		'filters': {'sucursal': "Norte"},
	// 		'fieldname': [
	// 			'name'
	// 		]
	// 	},
	// 	callback: function(r) {
	// 		if (!r.exc) {
	// 			// code snippet
	// 		}
			
	// 		console.log(r);
			
	// 		for(var i = 0; i < r.message.length; i++){
	// 			cajas.push(r.message[i].name);
	// 		}

	// 		frm.set_df_property("pos_name", "options", [cajas]);
	// 	}
	// });

	onload: function(frm) {
		var date = new Date;

		cur_frm.fields_dict['name_declaration'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'due_date': [">=",date]}
			}
		}

		cur_frm.fields_dict['pos_name'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'sucursal': doc.sucursal}
			}
		}	
	}
});
