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
	
	def on_update(self):
		self.create_user_POS_profile()
	
	def on_trash(self):
		self.delete_user_POS_profile()
	
	def delete_user_POS_profile(self):
		perfil = frappe.get_all("POS Profile User", ['name'], filters = {'user': self.user, 'parent': self.pos})

		for item in perfil:
			frappe.delete_doc('POS Profile User', item.name)
	
	def create_user_POS_profile(self):
		doc = frappe.get_doc('POS Profile', self.pos)
		row = doc.append("applicable_for_users", {})
		row.default = 1
		row.user = self.user
		doc.save()
	
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
