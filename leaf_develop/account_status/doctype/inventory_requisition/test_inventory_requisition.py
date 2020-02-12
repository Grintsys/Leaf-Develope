# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

def create_requisitions():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    doc = frappe.get_doc({
        "doctype": "Inventory Requisition",
		"name": "Test1",
        "patient_statement": 'Prueba',
		"date_create":'10-02-2020 15:34:04',
		"products": [{
			"item": 'CLI-SER-0003',
			"product_name": 'Colchon de agua',
			"quantity": 2
		}],
		"state": 'Open'
    }).insert()

    doc = frappe.get_doc({
        "doctype": "Inventory Requisition",
		"name": "Test2",
        "patient_statement": 'Prueba',
		"date_create":'10-02-2020 16:34:04',
		"products": [{
			"item": 'CLI-SER-0003',
			"product_name": 'Colchon de agua',
			"quantity": 2
		}],
		"state": 'Open'
    }).insert()

    doc = frappe.get_doc({
        "doctype": "Inventory Requisition",
		"name": "Test3",
        "patient_statement": 'Prueba',
		"date_create":'10-02-2020 17:34:04',
		"products": [{
			"item": 'CLI-SER-0003',
			"product_name": 'Colchon de agua',
			"quantity": 2
		}],
		"state": 'Open'
    }).insert()

    frappe.flags.test_events_created = True

class TestInventoryRequisition(unittest.TestCase):
	def setUp(self):
		create_requisitions()
	
	def tearDown(self):
		frappe.set_user("Administrator")

	def get_register(self):
		frappe.set_user("test1@example.com")
		doc = frappe.get_doc("Inventory Requisition", frappe.db.get_value("Inventory Requisition",{"name":"Test1"}))
		self.assertTrue(doc.name)