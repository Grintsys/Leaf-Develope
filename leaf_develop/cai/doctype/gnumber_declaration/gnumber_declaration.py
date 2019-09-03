# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class GNumberDeclaration(Document):
	def validate(self):
		self.validate_number_declaration()

	def validate_number_declaration(self):
		number_declaration = frappe.get_all("GNumber Declaration", filters = {"no_declaration": self.no_declaration})

		if len(number_declaration) != 0 and self.name != number_declaration[0].name:
			frappe.throw(_("This No. Declaration is using for other Number of Declaration."))
		
		if len(self.no_declaration) > 11:
			frappe.throw(_("You exceeded thw maximum number of characters valid for declaration number.")) 