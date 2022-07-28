# -*- coding: utf-8 -*-
# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DailyAccountStatement(Document):
	def validate(self):
		if self.created_by == None:
			self.created_by = frappe.session.user
			
		if self.docstatus == 0:
			self.return_data()
			
	def return_data(self):
		self.delete_rows()
		conditions = self.return_filters(self.from_date, self.to_date)

		results = frappe.get_all("Inventory Requisition", ["*"], filters = conditions)

		for result in results:
			if self.verificate_hours(result.date_create):
				items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": result.name})
				for item in items:
					acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
					price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})
					self.set_new_row_item(result.date_create, "Inventory Requisition", result.name, item.item, item.product_name, item.quantity, price[0].price)

		results = frappe.get_all("Hospital Outgoings", ["*"], filters = conditions)

		for result in results:
			if self.verificate_hours(result.date_create):
				items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": result.name})
				for item in items:
					acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
					price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})
					self.set_new_row_item(result.date_create, "Hospital Outgoings", result.name, item.item, item.product_name, item.quantity, price[0].price)

		results = frappe.get_all("Laboratory And Image", ["*"], filters = conditions)

		for result in results:
			if self.verificate_hours(result.date_create):
				items = frappe.get_all("Inventory Item", ["*"], filters = {"parent": result.name})
				for item in items:
					acc_sta = frappe.get_all("Account Statement Payment", ["name"], filters = {"patient_statement": self.patient_statement})
					price = frappe.get_all("Account Statement Payment Item Detail", ["*"], filters = {"parent": acc_sta[0].name, "item": item.item})
					self.set_new_row_item(result.date_create, "Laboratory And Image", result.name, item.item, item.product_name, item.quantity, price[0].price)
		
		conditions = self.return_filters_medical_honorarium()
		
		honorariums = frappe.get_all("Medical Honorarium", ["*"], filters = conditions)

		for honorarium in honorariums:
			items = frappe.get_all("Medical Honorarium Detail", ["*"], filters = {"parent": honorarium.name, "date": ["between", [self.from_date, self.to_date]]})

			for item in items:
				if self.verificate_hours(item.date):
					medical = frappe.get_doc("Medical", honorarium.medical)
					itemValues = frappe.get_doc("Item", medical.service)
					self.set_new_row_item(item.date, "Medical Honorarium", honorarium.name, medical.service, itemValues.item_name, 1, item.amount)
	
	def delete_rows(self):
		for row in self.get("detail_table"):
			frappe.delete_doc("Daily Account Statement Detail", row.name)

	def set_new_row_item(self, date, voucher_type, voucher_no, item, item_name, qty, amount):
		row = self.append("detail_table", {})
		row.date = date
		row.voucher_type = voucher_type
		row.voucher_no = voucher_no
		row.item = item
		row.item_name = item_name
		row.qty = qty
		row.amount = amount

	def verificate_hours(self, date):
		is_valid = False

		date_str = date.strftime('%Y-%m-%d %H:%M:%S')

		if date_str >= self.from_date:
			if date_str <= self.to_date:
				is_valid = True
		
		return is_valid

	def return_filters_medical_honorarium(self):
		conditions = ''	

		conditions += "{"
		conditions += '"patient_statement": "{}"'.format(self.patient_statement)
		conditions += ', "docstatus": 1'
		conditions += '}'

		return conditions

	def return_filters(self, from_date, to_date):
		conditions = ''	

		conditions += "{"
		conditions += '"date_create": ["between", ["{}", "{}"]]'.format(from_date, to_date)
		conditions += ', "patient_statement": "{}"'.format(self.patient_statement)
		conditions += ', "docstatus": 1'
		conditions += '}'

		return conditions

