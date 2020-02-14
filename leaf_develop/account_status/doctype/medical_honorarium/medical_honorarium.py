# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class MedicalHonorarium(Document):
	def validate(self):
		self.remaining()

	def remaining(self):
		if not self.total_remaining:
			if not self.total_payment:
				if(self.total > 0 and self.total_payment != 0):
					self.total_remaining = self.total
	