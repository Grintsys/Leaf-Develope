# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Returnofinventoryrequisition(Document):
	def validate(self):
		self.status()

	def status(self):
		if self.docstatus == 1:
			self.apply_changes("-")
			self.state = "Closed"
	
	def on_cancel(self):
		self.apply_changes("+")

	def apply_changes(self, signo):
		total_price = 0
		products = frappe.get_all("Inventory Item Return", ["item", "product_name", "quantity"], filters = {"parent": self.name})

		for item in products:		
			product_price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item})				

			if product_price:
				for product in product_price:			
					price = product.price_list_rate * item.quantity	
					total_price += price
			else:
				frappe.throw(_("{} does not have a defined price.".format(item.product_name)))

		doc = frappe.get_doc("Patient statement", self.patient_statement)
		if signo == "+":
			doc.cumulative_total += total_price
		
		if signo == "-":
			doc.cumulative_total -= total_price
		doc.save()
