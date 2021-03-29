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
		self.status()

	def on_update(self):
		payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.name})
		
		if len(payment) == 0:
			self.new_account_statement_payment()
	
	def status(self):
		if self.docstatus == 0:
			self.state = "Open"

		if self.docstatus == 1:
			self.state = "Closed"
			self.new_sale_invoice()
		
		if self.docstatus == 2:
			self.state = "Cancelled"
	
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

		inventory_requisitions = frappe.get_all("Inventory Requisition", ["name"], filters = {"patient_statement": self.name, "state": "Closed"})

		for inv_req in inventory_requisitions:
			products = frappe.get_all("Inventory Item", ["item", "quantity"], filters = {"parent": inv_req.name})

			for product in products:
				row = doc.append("items", {})
				row.item_code = product.item
				row.qty = product.quantity

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
