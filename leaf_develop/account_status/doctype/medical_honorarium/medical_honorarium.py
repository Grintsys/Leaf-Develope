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

		if self.docstatus == 0:
			self.patient_statement_acomulative_total("+")
	
	def on_cancel(self):
		self.patient_statement_acomulative_total("-")
	
	def on_trash(self):
		self.patient_statement_acomulative_total("-")

	def remaining(self):
		if not self.total_remaining:
			if not self.total_payment:
				if(self.total > 0 and self.total_payment != 0):
					self.total_remaining = self.total
	
	def patient_statement_acomulative_total(self, value):
		doc = frappe.get_doc("Patient statement", self.patient_statement)

		if value == "+":
			doc.outstanding_balance += self.total
			doc.cumulative_total += self.total
		
		if value == "-":
			doc.outstanding_balance -= self.total
			doc.cumulative_total -= self.total

		doc.save()