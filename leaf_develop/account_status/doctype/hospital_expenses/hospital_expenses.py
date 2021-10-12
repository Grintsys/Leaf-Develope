# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime

class HospitalExpenses(Document):
	def on_update(self):
		self.calculate_total()
		self.add_products_account_status_payment()

		if self.creation_date == None:
			self.creation_date = datetime.now()
	
	def on_cancel(self):
		self.delete_products_account_status_payment()
	
	def on_trash(self):
		self.delete_products_account_status_payment()
	
	def calculate_total(self):
		patient_statement = frappe.get_all("Patient statement", ["price_list"], filters = {"name": self.patient_statement})
		product_price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": self.service, "price_list": patient_statement[0].price_list})

		if len(product_price) == 0:
				frappe.throw(_("{} does not have a defined price in price list {}.".format(self.product_name, patient_statement[0].price_list)))

		hospital_expenses_detail = frappe.get_all("Hospital Expenses Detail", ["reason"], filters = {"parent": self.name})

		total_amount = product_price[0].price_list_rate * len(hospital_expenses_detail)

		self.db_set('total_amount', total_amount, update_modified=False)

	def add_products_account_status_payment(self):
		price = 0

		patient_statement = frappe.get_all("Patient statement", ["price_list"], filters = {"name": self.patient_statement})

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})

		product_price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": self.service, "price_list": patient_statement[0].price_list})

		hospital_expenses_detail = frappe.get_all("Hospital Expenses Detail", ["reason"], filters = {"parent": self.name})

		quantity = len(hospital_expenses_detail)
		
		if len(account_payment) == 0:
			frappe.throw(_("There is no invoice assigned hospital expenses detail to this statement."))

		product_verified = frappe.get_all("Account Statement Payment Item", ["name", "price"], filters = {"item": self.service, "price": product_price[0].price_list_rate, "parent": account_payment[0].name})

		if len(product_verified) > 0:
			price = quantity * product_price[0].price_list_rate
			doc_product = frappe.get_doc("Account Statement Payment Item", product_verified[0].name)
			doc_product.quantity = quantity
			doc_product.net_pay = price
			doc_product.sale_amount = price					
			doc_product.save()
		else:
			price = self.total_amount
			doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)					
			row = doc.append("products_table", {})
			row.item = self.service
			row.item_name = self.product_name
			row.quantity = quantity
			row.price = product_price[0].price_list_rate
			row.net_pay = price
			row.sale_amount = price
			row.reference = self.name
			doc.save()
				
		self.apply_changes()

	def delete_products_account_status_payment(self):
		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
		
		patient_statement = frappe.get_all("Patient statement", ["price_list"], filters = {"name": self.patient_statement})
		
		product_price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": self.service, "price_list": patient_statement[0].price_list})

		if len(product_price) == 0:
			frappe.throw(_("{} does not have a defined price in price list {}.".format(self.product_name, patient_statement[0].price_list)))

		hospital_expenses_detail = frappe.get_all("Hospital Expenses Detail", ["reason"], filters = {"parent": self.name})

		quantity = len(hospital_expenses_detail)
				
		product_verified = frappe.get_all("Account Statement Payment Item", ["name", "quantity", "price"], filters = {"item": self.service, "price": product_price[0].price_list_rate, "parent": account_payment[0].name})
			
		for product in product_verified:
			price = quantity * product.price

			if quantity > product.quantity:
				frappe.throw(_("The statement {} only one order an amount of {} for the product {}.".format(self.patient_statement, product.quantity, product.item_name)))

			if quantity == product.quantity:
				frappe.delete_doc("Account Statement Payment Item", product_verified[0].name)
			else:					
				doc_product = frappe.get_doc("Account Statement Payment Item", product_verified[0].name)
				doc_product.quantity = quantity
				doc_product.net_pay = price
				doc_product.sale_amount = price					
				doc_product.save()
		
		self.apply_changes()	

	def apply_changes(self):	
		total_price = 0

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
		
		account_payment_items = frappe.get_all("Account Statement Payment Item", ["name", "price", "net_pay"], filters = {"parent": account_payment[0].name})

		for item in account_payment_items:
			total_price += item.net_pay

		docu = frappe.get_doc("Account Statement Payment", account_payment[0].name)
		docu.total = total_price
		docu.outstanding_balance = docu.total - docu.total_advance
		docu.save()