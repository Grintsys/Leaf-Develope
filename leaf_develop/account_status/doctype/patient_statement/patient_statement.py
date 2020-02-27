# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta, date

class Patientstatement(Document):
	def on_update(self):
		self.new_account_statement_payment()
	
	def new_account_statement_payment(self):
		doc = frappe.new_doc('Account Statement Payment')
		doc.patient_statement = self.name
		doc.date = self.date
		doc.customer = self.client
		doc.insert()
	
	def on_trash(self):
		self.delete_account_statement_payment()
	
	def delete_account_statement_payment(self):
		payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.name})

		for item in payment:
			doc = frappe.delete_doc("Account Statement Payment", item.name)
