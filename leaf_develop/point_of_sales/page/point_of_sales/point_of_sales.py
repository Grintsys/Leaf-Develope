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
	pos = frappe.get_value('GCAI Allocation',{"user":user},["pos","branch"],as_dict =1)
	if pos is None:
		frappe.throw("no GCAI Allocation")

	configs = frappe.get_all("Point Of Sale Profile",["*"],filters = {"cashier_name": pos.pos})
	config = next(iter(configs),None)
	if config is None:
		frappe.throw("no Point Of Sale Profile")
	
	config.credential = frappe.utils.password.get_decrypted_password('Point Of Sale Profile',config.name,'credential')
	
	payments_Methods = frappe.get_all("Sales Invoice Payment",["mode_of_payment"],filters = {"parent":config.name})
	config.paymentMethods = []
	for payment_Method in payments_Methods:
		config.paymentMethods.append(payment_Method.mode_of_payment)

	item_groups = frappe.get_all("POS Item Group",["item_group"],filters = {"parent":config.name})
	config.itemGroups = []
	for item_group in item_groups:
		config.itemGroups.append(item_group.item_group)


	customer_groups = frappe.get_all("POS Customer Group",["customer_group"],filters = {"parent":config.name})

	config.customerGroup = []
	for customer_group in customer_groups:
		config.customerGroup.append(customer_group.customer_group)


	config.requiresOpening = True

	openings = frappe.get_all("Opening POS",["*"],filters = {"cashier": pos.pos,"branch":pos.branch},order_by = "creation desc") 
	lastOpening = next(iter(openings),None)
	if lastOpening is None:
		return config

	clousures = frappe.get_all("Close Pos",["*"],filters = {"pos": pos.pos,"sucursal":pos.branch},order_by = "creation desc") 
	lastClousure = next(iter(clousures),None)
	if lastClousure is None:
		config.requiresOpening = False
		return config

	if lastOpening.creation > lastClousure.creation:
		config.requiresOpening = False

	return config


