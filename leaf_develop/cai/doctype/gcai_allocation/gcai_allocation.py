# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class GCAIAllocation(Document):
	
	def validate(self):
		self.validate_pos()
		self.validate_user()
	
	def validate_pos(self):
		pos = frappe.get_all("GPos", ["name"], filters = {"name": self.pos, "sucursal": self.branch})

		if len(pos) == 0:
			frappe.throw(_("This post does not belong to this branch"))

	def validate_user(self):
		user = frappe.get_all("GCAI Allocation", ["user"], filters = {"user": self.user})

		if len(user) != 0:
			frappe.throw(_("This user has already been assigned a cai"))
