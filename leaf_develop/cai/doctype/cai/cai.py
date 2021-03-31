# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.permissions import get_doctypes_with_read
from frappe.model.naming import parse_naming_series

class CAI(Document):
	def get_transactions(self, arg=None):
		doctypes = list(set(frappe.db.sql_list("""select parent
				from `tabDocField` df where fieldname='naming_series'""")
			+ frappe.db.sql_list("""select dt from `tabCustom Field`
				where fieldname='naming_series'""")))

		doctypes = list(set(get_doctypes_with_read()).intersection(set(doctypes)))

		return {
			"transactions": doctypes
		}

	def get_prefix(self, arg=None):
		transaction = self.select_doc_for_series
		prefixes = ""
		options = ""
		try:
			options = self.get_options(transaction)
		except frappe.DoesNotExistError:
			frappe.msgprint(_('Unable to find DocType {0}').format(d))

		if options:
			prefixes = prefixes + "\n" + options

		prefixes.replace("\n\n", "\n")
		prefixes = prefixes.split("\n")
		prefixes = "\n".join(sorted(prefixes))

		return {
			"prefix": prefixes
		}


	def get_options(self, arg=None):
		if frappe.get_meta(arg or self.select_doc_for_series).get_field("naming_series"):
			return frappe.get_meta(arg or self.select_doc_for_series).get_field("naming_series").options
	
	def before_insert(self):
		cai = frappe.get_all("CAI", ["cai"], filters = { "status": "Active", "prefix": self.prefix})
		if len(cai) > 0:
			self.status = "Pending"
		else:
			self.status = "Active"
			new_current = int(self.initial_number) - 1
			name = self.parse_naming_series(self.prefix)

			frappe.db.set_value("Series", name, "current", new_current, update_modified=False)
	
	def parse_naming_series(self, prefix):
		parts = prefix.split('.')
		if parts[-1] == "#" * len(parts[-1]):
			del parts[-1]

		pre = parse_naming_series(parts)
		return pre