# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class InventoryRequisition(Document):
	def validate(self):
		self.status()

	def status(self):
		if self.docstatus == 1:
			self.apply_changes("+")
			self.add_products_account_status_payment()
			self.state = "Closed"
	
	def on_cancel(self):
		self.apply_changes("-")
		self.delete_products_account_status_payment()
		self.state = "Cancelled"

	def apply_changes(self, signo):
		total_price = 0
		products = frappe.get_all("Inventory Item", ["item", "product_name", "quantity"], filters = {"parent": self.name})

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
			doc.outstanding_balance += total_price
		
		if signo == "-":
			doc.cumulative_total -= total_price
			doc.outstanding_balance -= total_price
		doc.save()
	
	def add_products_account_status_payment(self):
		products = frappe.get_all("Inventory Item", ["item", "product_name", "quantity"], filters = {"parent": self.name})

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
		
		if len(account_payment) == 0:
			frappe.throw(_("There is no invoice assigned to this statement."))

		for item in products:
			product_price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item})	

			for product in product_price:
				doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)
				price = item.quantity * product.price_list_rate
				isv = price * (15/100)
				row = doc.append("products_table", {})
				row.item = item.item
				row.item_name = item.product_name
				row.quantity = item.quantity
				row.price = product.price_list_rate
				row.net_pay = price
				row.reference = self.name
				doc.total += price
				doc.isv15 += isv
				doc.net_total += price + isv
				doc.save()
	
	def delete_products_account_status_payment(self):
		accounts_payments = frappe.get_all("Account Statement Payment", ["name"], filters = {"reference": self.name})

		for account in accounts_payments:
			frappe.delete_doc("Account Statement Payment", account.name)