# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
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
			"item": 'CLI-MVA-0008',
			"product_name": 'Alergil Jarabe',
			"quantity": 2
		}],
		"state": 'Open'
    }).insert()

    frappe.flags.test_events_created = True

class TestInventoryRequisition(unittest.TestCase):
	def setUp(self):
		create_requisitions()

	def get_register(self):
		frappe.set_user("test1@example.com")
		doc = frappe.get_doc("Inventory Requisition", frappe.db.get_value("Inventory Requisition",{"name":"Test1"}))
		self.assertEquals(len(doc), 1)