# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import date
from datetime import datetime

class HospitalExpenses(Document):
	def validate(self):
		self.status()

	def status(self):
		# if self.docstatus == 0:
		# 	self.add_products_account_status_payment()

		if self.docstatus == 1:
			# self.material_request()
			self.state = "Closed"
	
	def on_update(self):
		if self.docstatus == 0:
			self.add_products_account_status_payment()
	
	def on_cancel(self):
		self.delete_products_account_status_payment()
		self.state = "Cancelled"
	
	def on_trash(self):
		self.delete_products_account_status_payment()

	def apply_changes(self, total_price):		
		doc = frappe.get_doc("Patient statement", self.patient_statement)
		doc.cumulative_total += total_price
		doc.outstanding_balance += total_price
		doc.save()

		acc_sta_pay = frappe.get_all("Account Statement Payment", {"name"}, filters = {"patient_statement" : self.patient_statement})
		docu = frappe.get_doc("Account Statement Payment", acc_sta_pay[0].name)
		docu.outstanding_balance += total_price
		docu.save()
	
	def material_request(self):
		products = frappe.get_all("Inventory Item", ["item", "quantity"], filters = {"parent": self.name})
		warehouse = frappe.get_all("Patient Warehouse", ["name_warehouse"])

		if len(warehouse) == 0:
			frappe.throw("There is no Patient Warehouse to assign, create a new one.")

		now = datetime.now()

		doc = frappe.new_doc('Material Request')
		doc.schedule_date = now
		doc.material_request_type = 'Material Transfer'
		doc.requested_by = self.patient_statement
		for list_product in products:
			row = doc.append("items", {
				'item_code': list_product.item,
				'qty': list_product.quantity,
				'schedule_date': now,
				'warehouse': warehouse[0].name_warehouse
				})
		doc.save()
	
	def add_products_account_status_payment(self):
		total_price = 0
		products = frappe.get_all("Inventory Item", ["item", "product_name", "quantity", "name"], filters = {"parent": self.name, "add": 0})

		patient_statement = frappe.get_all("Patient statement", ["price_list"], filters = {"name": self.patient_statement})

		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
		
		if len(account_payment) == 0:
			frappe.throw(_("There is no invoice assigned to this statement."))

		for item in products:
			product_price = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item.item, "price_list": patient_statement[0].price_list})			

			if len(product_price) == 0:
				frappe.throw(_("{} does not have a defined price in price list {}.".format(item.product_name, patient_statement[0].price_list)))

			for product in product_price:
				price = item.quantity * product.price_list_rate
				product_verified = frappe.get_all("Account Statement Payment Item", ["name", "price"], filters = {"item": item.item, "parent": account_payment[0].name})

				if len(product_verified) > 0:
					price = item.quantity * product_verified[0].price
					total_price += price
					doc_product = frappe.get_doc("Account Statement Payment Item", product_verified[0].name)
					doc_product.quantity += item.quantity
					doc_product.net_pay += price
					doc_product.sale_amount += price						
					doc_product.save()

					doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)
					doc.total += price
					doc.outstanding_balance = doc.total - doc.total_advance
					doc.save()

					docItem = frappe.get_doc("Inventory Item", item.name)
					# # docItem.db_set('add', 1, update_modified=False)
					docItem.add = 1
					docItem.save(ignore_permissions=True, ignore_version=True)
				else:
					total_price += price
					doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)					
					row = doc.append("products_table", {})
					row.item = item.item
					row.item_name = item.product_name
					row.quantity = item.quantity
					row.price = product.price_list_rate
					row.net_pay = price
					row.sale_amount = price
					row.reference = self.name
					doc.total += price
					doc.outstanding_balance = doc.total - doc.total_advance
					doc.save()

					docItem = frappe.get_doc("Inventory Item", item.name)
					# # docItem.db_set('add', 1, update_modified=False)
					docItem.add = 1
					docItem.save(ignore_permissions=True, ignore_version=True)
			
		# self.apply_changes(total_price)
	
	def delete_products_account_status_payment(self):
		total_price = 0
		account_payment = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
		products = frappe.get_all("Inventory Item", ["item", "product_name", "quantity"], filters = {"parent": self.name})

		if len(account_payment) == 0:
			return

		for item in products:
			product_verified = frappe.get_all("Account Statement Payment Item", ["name", "quantity", "price"], filters = {"item": item.item, "parent": account_payment[0].name})
			
			for product in product_verified:
				price = item.quantity * product.price
				total_price -= price

				if item.quantity > product.quantity:
					frappe.throw(_("The statement {} only one order an amount of {} for the product {}.".format(self.patient_statement, product.quantity, product.item_name)))

				if item.quantity == product.quantity:
					frappe.delete_doc("Account Statement Payment Item", product_verified[0].name)
				else:					
					doc_product = frappe.get_doc("Account Statement Payment Item", product_verified[0].name)
					doc_product.quantity -= item.quantity
					doc_product.net_pay -= price	
					doc_product.sale_amount -= price				
					doc_product.save()

				doc = frappe.get_doc("Account Statement Payment", account_payment[0].name)
				doc.total -= price
				doc.save()
		
		self.apply_changes(total_price)
