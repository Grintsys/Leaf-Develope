# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

test_records = frappe.get_test_records('Medical Category')

def create_events():
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype":"Medical Category",
		"rank": "Medico General"
    }).insert()

class TestMedicalCategory(unittest.TestCase):
	def setUp(self):
		create_events()

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_create_medical(self):
		frappe.set_user("admin@example.com")
		doc = frappe.get_doc("Medical Category", frappe.db.get_value("Medical Category",{"rank":"Medico General"}))
		self.assertTrue(doc.rank)
