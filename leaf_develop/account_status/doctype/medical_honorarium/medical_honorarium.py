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
		if self.docstatus == 1:
			self.remaining()
			self.verificate_changes()

			self.add_medical_honorarium_payment()
	
	def on_cancel(self):
		self.delete_products_account_status_payment()
	
	def on_trash(self):
		self.delete_products_account_status_payment()

	def remaining(self):
		if not self.total_remaining:
			if not self.total_payment:
				if(self.total > 0 and self.total_payment != 0):
					self.total_remaining = self.total
	
	def apply_changes(self, total):
		doc = frappe.get_doc("Patient statement", self.patient_statement)
		doc.outstanding_balance += total
		doc.cumulative_total += total
		doc.save()

	def verificate_changes(self):
		now = frappe.get_all("Medical Honorarium", filters={'name': self.name}, fields={"total", "medical", "date", "patient_statement"})
		for item in now:
			if item.total != self.total:
				self.total_remaining = self.total
				self.condition_for_changes()
			elif item.medical != self.medical:
				self.condition_for_changes()
			elif item.patient_statement != self.patient_statement:
				self.condition_for_changes()

	def condition_for_changes(self):
		honorarium_payment = frappe.get_all("Honorarium Payment", filters={'honorarium': self.name})
		if len(honorarium_payment) > 0:
			frappe.throw(_("The fee cannot be edited because you already have a payment made"))

	def add_medical_honorarium_payment(self):
		total_price = 0
		medico = frappe.get_all("Medical", ["service"], filters = {'name': self.medical})

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})

		if len(account_payment) == 0:
			frappe.throw(_("There is no invoice assigned to this statement."))

		for item in medico:
			price = self.wire_tranfser_total
			total_price += price
			
			products = frappe.get_all("Item", ["item_name"], filters = {'name': item.service})	

			ver_product = frappe.get_all("Account Statement Payment Item", ["name", "price"], filters = {"item": item.service, "reference": self.name})	

			if len(ver_product) > 0:
				price_ver = ver_product[0].price
				doc = frappe.get_doc("Account Statement Payment Item", ver_product[0].name)				
				doc.price = price
				doc.save()

				total_price = price - price_ver

				doc_acc = frappe.get_doc("Account Statement Payment", account_payment[0].name)
				doc_acc.total += total_price
				doc_acc.save()
				
				self.apply_changes(total_price)
				total_price = 0
				break

			for product in products:							
				doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)					
				row = doc.append("products_table", {})
				row.item = item.service
				row.item_name = product.item_name
				row.quantity = 1
				row.price = price
				row.net_pay = price
				row.reference = self.name
				doc.total += price
				doc.save()
			
		self.apply_changes(total_price)

	def delete_products_account_status_payment(self):
		total_price = 0
		medico = frappe.get_all("Medical", ["service"], filters = {'name': self.medical})

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})

		if len(account_payment) == 0:
			return

		for item in medico:				

			product_verified = frappe.get_all("Account Statement Payment Item", ["name", "quantity", "price"], filters = {"item": item.service, "parent": account_payment[0].name, "reference": self.name})

			for product in product_verified:
				price = product.price
				total_price -= price

				frappe.delete_doc("Account Statement Payment Item", product.name)

				doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)
				doc.total -= price
				doc.save()	

		self.apply_changes(total_price)
	
	def on_update(self):
		self.calculate_totals()
		self.remaining()
		self.verificate_changes()

		self.add_medical_honorarium_payment()
	
	def calculate_totals(self):
		cash_total = 0
		wire_tranfser_total = 0
		details = frappe.get_all("Medical Honorarium Detail", ["amount", "transaction_payment"], filters = {"parent": self.name})

		for detail in details:
			if detail.transaction_payment == "Cash":
				cash_total += detail.amount
			
			if detail.transaction_payment == "Wire Transfer":
				wire_tranfser_total += detail.amount

		self.cash_total = cash_total
		self.wire_tranfser_total = wire_tranfser_total
		self.total = cash_total + wire_tranfser_total
		