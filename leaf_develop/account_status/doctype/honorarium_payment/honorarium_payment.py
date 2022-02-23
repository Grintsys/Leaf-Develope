# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document

class HonorariumPayment(Document):
	def validate(self):
		self.verificate_status_honorarium()
		if(self.total > self.honorarium_amount):
			frappe.throw(_("The amount cannot be greater than the total honorarium"))

		self.verificate()
		remaining = self.honorarium_amount - self.total
		self.total_remaining = remaining
		if self.docstatus == 1:
			self.calculate_honorarium()
	
	def calculate_honorarium(self):
		validate = False
		doc = frappe.get_doc("Medical Honorarium", self.honorarium)
		if doc.docstatus == 1:
			validate = True
			doc.db_set('docstatus', 0, update_modified = False)

		if(self.total == self.honorarium_amount):
			if(self.total_remaining == 0):
				doc.status = "Paid Out"
				doc.total_payment += self.total
				doc.total_remaining -= self.total
		else:
			if(self.total < self.honorarium_amount):
				if(self.total_remaining > 0):
					doc.status = "Open"
					doc.total_payment += self.total
					doc.total_remaining -= self.total
		doc.save()

		self.data_table(validate)
	
	def on_cancel(self):
		self.status()
	
	def verificate(self):
		if(self.total == self.honorarium_amount and self.type_payment == "Advancement"):
			frappe.throw(_("The type of payment cannot be an advance"))
		if(self.total < self.honorarium_amount and self.type_payment == "Payment"):
			frappe.throw(_("The type of payment must be an advance"))

	def status(self):
		doc = frappe.get_doc("Medical Honorarium", self.honorarium)
		doc.total_payment -= self.total
		doc.total_remaining += self.total
		if(doc.status == "Paid Out"):
			doc.status = "Open"

		doc.save()
		honorarium = frappe.get_all("Honorarium Payment Detail", ["name"], filters={"series": self.name})
		for item in honorarium:
			frappe.delete_doc("Honorarium Payment Detail", item.name)
			

	def data_table(self, validate):
		doc = frappe.get_doc("Medical Honorarium", self.honorarium)
		row = doc.append("honorarium_payment", {
			'series': self.name,
			'full_name': self.full_name,
			'total': self.total,
			'type_payment': self.type_payment,
			'transaction_payment': self.transaction_payment
			})
		doc.save()

		if validate:
			doc.db_set('docstatus', 1, update_modified = False)

	def verificate_status_honorarium(self):
		doc = frappe.get_doc("Medical Honorarium", self.honorarium)

		if(doc.status == "Paid Out"):
			frappe.throw(_("There is no remaining balance for the honorarium {}".format(self.honorarium)))
