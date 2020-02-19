# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class GCaiSettings(Document):
	
	def validate(self):
		self.validate_registers()
	
	def validate_registers(self):
		data = frappe.get_all("GCai Settings", ["name"])

		if len(data) > 0:
			frappe.throw(_("{}".format("A configuration already exists, modify the existing registry")))
