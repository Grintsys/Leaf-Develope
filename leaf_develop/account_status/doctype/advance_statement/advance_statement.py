# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class AdvanceStatement(Document):
	def validate(self):
		self.status()

	def status(self):
		if self.docstatus == 1:
			self.apply_changes("+")
			self.state = "Closed"
	
	def on_cancel(self):
		self.apply_changes("-")
		self.state = "Cancelled"

	def apply_changes(self, signo):
		doc = frappe.get_doc("Patient statement", self.patient_statement)
		if doc.cumulative_total > 0:
			if signo == "+":
				doc.total_advance += self.amount
				doc.outstanding_balance -= self.amount
		
			if signo == "-":
				doc.total_advance -= self.amount
				doc.outstanding_balance += self.amount

		doc.save()