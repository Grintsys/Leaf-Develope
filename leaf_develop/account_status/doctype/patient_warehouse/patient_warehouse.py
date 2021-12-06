# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class PatientWarehouse(Document):
	def get_prefix(self, arg=None):
		prefixes = ""
		options = ""
		try:
			options = self.get_options('Sales Invoice')
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
