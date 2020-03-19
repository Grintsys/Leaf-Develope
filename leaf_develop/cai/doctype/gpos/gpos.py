# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class GPos(Document):

	def validate(self):
		self.validate_branch()

	def on_update(self):
		self.create_POS_perfil()
	
	def create_POS_perfil(self):
		doc = frappe.new_doc('POS Profile')
		doc.name = self.name
		doc.insert()
	
	def delete_POS_perfil(self):
		frappe.delete_doc('POS Profile', self.name)

	def validate_branch(self):
		sucursal = frappe.get_all("GSucursal", ["name"], filters = {"name": self.sucursal, "company": self.company})

		if len(sucursal) == 0:
			frappe.throw(_("This branch does not belong to this company"))

	def on_trash(self):
		self.delete_POS_perfil()
		self.validate_delete()

	def validate_delete(self):
		user = frappe.get_all("GCAI Allocation", ["user"], filters = {"pos": self.name})

		if len(user) != 0:
			frappe.throw(_("This pos is associated with an User"))
