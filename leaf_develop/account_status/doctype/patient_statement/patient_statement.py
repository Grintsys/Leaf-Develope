# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta, date
from frappe.permissions import get_doctypes_with_read

class Patientstatement(Document):
	def validate(self):
		self.calculate_age()
		self.status()

	def on_update(self):
		payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.name})
		
		if len(payment) == 0:
			self.new_account_statement_payment()
	
	def status(self):
		if self.docstatus == 0:
			self.state = "Open"

		if self.docstatus == 1:
			if self.acc_sta == "Open":
				frappe.throw(_("This Patient Statement is open."))
				
			self.state = "Closed"
			self.new_sale_invoice()
		
		if self.docstatus == 2:
			self.state = "Cancelled"
	
	def new_account_statement_payment(self):
		doc = frappe.new_doc('Account Statement Payment')
		doc.patient_statement = self.name
		doc.date = self.date
		doc.customer = self.client
		doc.reason_for_sale = self.reason_for_sale
		doc.insert()
	
	def on_trash(self):
		self.delete_account_statement_payment()
	
	def delete_account_statement_payment(self):
		payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.name})

		if len(payment) > 0:
			for item in payment:
				doc = frappe.delete_doc("Account Statement Payment", item.name)
	
	def new_sale_invoice(self):
		now = datetime.now()
		doc = frappe.new_doc('Sales Invoice')
		doc.naming_series = self.naming_series
		doc.patient_statement = self.name
		doc.due_date = now.date()
		doc.customer = self.client
		doc.reason_for_sale = self.reason_for_sale
		doc.patient = self.patient
		doc.selling_price_list = self.price_list
		doc.ignore_pricing_rule = 1

		payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.name})
		
		items = frappe.get_all("Account Statement Payment Item", ["item", "item_name", "quantity", "price", "net_pay", "sale_amount"], filters = {"parent": payment[0].name})

		for item in items:
			row = doc.append("items", {})
			row.item_code = item.item
			row.qty = item.quantity

			if item.net_pay != item.sale_amount:
				row.rate = item.sale_amount
			else:
				row.rate = item.price

		doc.save()

	def get_prefix(self, arg=None):
		prefixes = ""
		options = ""
		try:
			options = self.get_options('Sales Invoice')
		except frappe.DoesNotExistError:
			frappe.msgprint(_('Unable to find DocType {0}').format(d))

		if options:
			prefixes = prefixes + "\n" + options

		prefixes.replace("\n\n", "\n")
		prefixes = prefixes.split("\n")
		prefixes = "\n".join(sorted(prefixes))

		return {
			"prefix": prefixes
		}


	def get_options(self, arg=None):
		if frappe.get_meta(arg or self.select_doc_for_series).get_field("naming_series"):
			return frappe.get_meta(arg or self.select_doc_for_series).get_field("naming_series").options
	
	def calculate_age(self):
		patient = frappe.get_doc("Patient", self.patient)

		if patient.dob != None:
			today = date.today()
			self.age = today.year - patient.dob.year - ((today.month, today.day) < (patient.dob.month, patient.dob.day))
		else:
			frappe.msgprint(_("Pacient has no date of birthday"))
