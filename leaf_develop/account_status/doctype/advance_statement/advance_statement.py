# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import money_in_words
from datetime import datetime

class AdvanceStatement(Document):
	def validate(self):
		self.status()

		self.in_words = money_in_words(self.amount)
		self.cashier = frappe.session.user

	def on_update(self):
		self.calculate_amount()
	
	def before_naming(self):
		self.date_create = datetime.today()

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
	
	def calculate_amount(self):
		amount = 0
		self.amount = 0
		for pay in self.get("payments"):
			self.amount += pay.amount
			amount += pay.amount
		
		self.db_set('amount', amount, update_modified=False)