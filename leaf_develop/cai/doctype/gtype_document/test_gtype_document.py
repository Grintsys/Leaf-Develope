# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

test_records = frappe.get_test_records('GType Document')
model = "GType Document"

def default_data():
	return {
	    "doctype":"GType Document",
		"name": "Factura",
		"number": "001"
	}

def create_events():

	if frappe.flags.test_events_created:
		return
		
	register = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": register["doctype"],
		"name": register["name"],
		"number": register["number"]
    }).insert()

	frappe.flags.test_events_created = True

class TestGTypeDocument(unittest.TestCase):
	def setUp(self):
		create_events()

	def test_create_register_TRUE(self):
		register = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("GType Document", frappe.db.get_value("GType Document",{"number": register["number"]}))
		self.assertEquals(doc.number,"001")
