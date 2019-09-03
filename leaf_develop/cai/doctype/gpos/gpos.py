# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class GPos(Document):
	 
	def on_trash(self):
		self.validate_delete()

	def validate_delete(self):
		user = frappe.get_all("GCAI Allocation", ["user"], filters = {"pos": self.name})

		if len(user) != 0:
			frappe.throw(_("This pos is associated with an User"))
