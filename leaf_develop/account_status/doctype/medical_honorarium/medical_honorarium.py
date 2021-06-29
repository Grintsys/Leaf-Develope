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
			self.apply_changes(self.total, self.bank_check)
	# 		self.remaining()
	# 		self.verificate_changes()

	# 		self.add_medical_honorarium_payment()
	
	def on_cancel(self):
		self.delete_products_account_status_payment()
	
	def on_trash(self):
		self.delete_products_account_status_payment()

	def remaining(self):
		if not self.total_remaining:
			if not self.total_payment:
				if(self.total > 0 and self.total_payment != 0):
					self.db_set('total_remaining', self.total, update_modified=False)
	
	def apply_changes(self, total, bank_check):
		doc = frappe.get_doc("Patient statement", self.patient_statement)
		doc.outstanding_balance += bank_check
		doc.cumulative_total += bank_check
		doc.save()

		acc_sta_pay = frappe.get_all("Account Statement Payment", {"name"}, filters = {"patient_statement" : self.patient_statement})
		docu = frappe.get_doc("Account Statement Payment", acc_sta_pay[0].name)
		docu.outstanding_balance += total
		docu.save()

	def verificate_changes(self):
		now = frappe.get_all("Medical Honorarium", filters={'name': self.name}, fields={"total", "medical", "date", "patient_statement"})
		for item in now:
			if item.total != self.total_remaining:
				self.db_set('total_remaining', self.total, update_modified=False)
				self.condition_for_changes()
			elif item.medical != self.medical:
				self.condition_for_changes()
			elif item.patient_statement != self.patient_statement:
				self.condition_for_changes()

	def condition_for_changes(self):
		total = 0
		honorarium_payment = frappe.get_all("Honorarium Payment", filters={'honorarium': self.name}, fields={"total"})

		for honorarium in honorarium_payment:
			total += honorarium.total

		if total > self.total:
			frappe.throw(_("The rate cannot be edited because you have already paid the invoice total or your last payment exceeds the total fee."))
		
		self.db_set('total_remaining', self.total - total, update_modified=False)

	def add_medical_honorarium_payment(self):
		total_price = 0
		medico = frappe.get_all("Medical", ["service"], filters = {'name': self.medical})

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})

		if len(account_payment) == 0:
			frappe.throw(_("There is no invoice assigned to this statement."))

		for item in medico:
			price = self.total
			total_price += price
			
			products = frappe.get_all("Item", ["item_name"], filters = {'name': item.service})	

			ver_product = frappe.get_all("Account Statement Payment Item", ["name", "price"], filters = {"item": item.service, "reference": self.name})	

			if len(ver_product) > 0:
				price_ver = ver_product[0].price
				doc = frappe.get_doc("Account Statement Payment Item", ver_product[0].name)				
				doc.price = price
				doc.net_pay = price
				doc.sale_amount = self.bank_check
				doc.save()

				total_price = price - price_ver

				doc_acc = frappe.get_doc("Account Statement Payment", account_payment[0].name)
				doc_acc.total += total_price
				doc_acc.outstanding_balance = doc_acc.total - doc_acc.total_advance
				doc_acc.save()

				# self.apply_changes(total_price)
					
				total_price = 0
				break

			else:

				for product in products:							
					doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)					
					row = doc.append("products_table", {})
					row.item = item.service
					row.item_name = product.item_name
					row.quantity = 1
					row.price = price
					row.net_pay = price
					row.sale_amount = self.bank_check
					row.reference = self.name
					doc.total += price
					doc.outstanding_balance = doc.total - doc.total_advance
					doc.save()

				# self.apply_changes(self.bank_check)

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

		bank_check = self.bank_check - (self.bank_check * 2)

		self.apply_changes(total_price, bank_check)
	
	def on_update(self):
		total = 0
		honorarium_payment = frappe.get_all("Honorarium Payment", filters={'honorarium': self.name}, fields={"total"})

		for honorarium in honorarium_payment:
			total += honorarium.total

		if self.status != "Paid Out" or total <= self.total:
			self.calculate_totals()
			self.remaining()
			self.verificate_changes()

			self.add_medical_honorarium_payment()
		else:
			frappe.throw(_("This Medical Honorarium Paid Out."))
	
	def calculate_totals(self):
		cash_total = 0
		bank_check = 0
		details = frappe.get_all("Medical Honorarium Detail", ["amount", "transaction_payment"], filters = {"parent": self.name})

		for detail in details:
			if detail.transaction_payment == "Cash":
				cash_total += detail.amount
			
			if detail.transaction_payment == "Bank Check":
				bank_check += detail.amount

		self.db_set('cash_total', cash_total, update_modified=False)
		self.db_set('bank_check', bank_check, update_modified=False)
		self.db_set('total', cash_total + bank_check, update_modified=False)

		total_honorarium_payment = 0
		honorarium_payment = frappe.get_all("Honorarium Payment", filters={'honorarium': self.name}, fields={"total"})

		for honorarium in honorarium_payment:
			total_honorarium_payment += honorarium.total
		
		self.db_set('total_remaining', cash_total + bank_check - total_honorarium_payment, update_modified=False)
		