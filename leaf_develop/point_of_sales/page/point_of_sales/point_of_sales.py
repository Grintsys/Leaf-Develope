# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.utils.nestedset import get_root_of
from frappe.utils import cint
from erpnext.accounts.doctype.pos_profile.pos_profile import get_item_groups

from six import string_types

@frappe.whitelist()
def item(item):
	data = ""
	json = {}
	items = frappe.get_all("Item", ["item_name", "item_code"], filters = {"name": item})
	for item_selected in items:
		item_prices = frappe.get_all("Item Price", ["price_list_rate"], filters = {"item_code": item_selected.item_code})
		for price in item_prices:
			json = {
				'item_code': item_selected.item_code,
				'item_name': item_selected.item_name,
				'price_cu': str(price.price_list_rate),
				'total': str(price.price_list_rate)
			}

	if len(items) > 0 and len(item_prices) > 0:
		data = items[0].item_name + "," + str(item_prices[0].price_list_rate) + "," + str(item_prices[0].price_list_rate)

	return json

@frappe.whitelist()
def get_item_max_discount(item_code):
	item = frappe.get_all("Item",["max_discount"],filters = {"item_code": item_code})

	return item[0].max_discount 


@frappe.whitelist()
def get_customer_rtn(customer_name):
	customers = frappe.get_all("Customer",["rtn","customer_default"],filters = {"customer_name": customer_name})
	json = {}
	for customer in customers:
			json = {
				'customer_default': customer.customer_default,
				'rtn': customer.rtn,
			}
	
	return json

@frappe.whitelist()
def get_pos_config():
	user = frappe.session.user
	pos = frappe.get_value('GCAI Allocation',{"user":user},["pos"],as_dict =1)
	print(user)
	return user