# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import money_in_words

class AdvanceStatement(Document):
	def validate(self):
		self.status()

		self.in_words = money_in_words(self.amount)
		self.cashier = frappe.session.user

	def status(self):
		if self.docstatus == 1:
			self.apply_changes("+")
			self.state = "Closed"
	
	def on_cancel(self):
		self.apply_changes("-")
		self.state = "Cancelled"

	def apply_changes(self, signo):
		doc = frappe.get_doc("Patient statement", self.patient_statement)

		acc_sta_pay = frappe.get_all("Account Statement Payment", {"name"}, filters = {"patient_statement" : self.patient_statement})

		docu = frappe.get_doc("Account Statement Payment", acc_sta_pay[0].name)
		
		if signo == "+":
			doc.total_advance += self.amount
			doc.outstanding_balance -= self.amount
			docu.total_advance += self.amount
			docu.outstanding_balance -= self.amount
		
		if signo == "-":
			doc.total_advance -= self.amount
			doc.outstanding_balance += self.amount
			docu.total_advance -= self.amount
			docu.outstanding_balance += self.amount

		doc.save()
		docu.save()