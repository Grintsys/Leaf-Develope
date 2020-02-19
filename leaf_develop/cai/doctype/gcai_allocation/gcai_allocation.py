# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class GCAIAllocation(Document):
	
	def validate(self):
		self.validate_pos_and_sucursal()
		self.validate_user()
	
	def validate_pos_and_sucursal(self):
		pos = frappe.get_all("GPos", ["name"], filters = {"name": self.pos, "sucursal": self.branch})
		sucursal = frappe.get_all("GSucursal", ["name"], filters = {"name": self.branch, "company": self.company})

		if len(sucursal) == 0:
			frappe.throw(_("This branch does not belong to this company"))

		if len(pos) == 0:
			frappe.throw(_("This pos does not belong to this branch"))
		

	def validate_user(self):
		user = frappe.get_all("GCAI Allocation", ["name"], filters = {"user": self.user, "company": self.company, "type_document": self.type_document})
		
		if len(user) != 0:
			if user[0].name != self.name:
				frappe.throw(_("This user has already been assigned a cai for this type component in the company."))
