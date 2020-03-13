# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest
test_records = frappe.get_test_records('Medical Honorarium')
model = "Medical Honorarium"

def default_data():
	return {
		"doctype":"Medical Honorarium",
		"date": "17-02-2020",
		"medical": "AS-MA-00001",
		"patient_statement": "Nuevo",
		"total": 20000
	}

def create_events():
	if frappe.flags.test_events_created:
		return

	honorarium = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": honorarium["doctype"],
		"date": honorarium["date"],
		"medical": honorarium["medical"],
		"patient_statement": honorarium["patient_statement"],
		"total": honorarium["total"]
    }).insert()

	frappe.flags.test_events_created = True

class TestMedicalHonorarium(unittest.TestCase):
	def non_commit(self):
		frappe.set_user("Administrator")
		pass

	def setUp(self):
		frappe.set_user("Administrator")
		create_events()
		frappe.db.commit = self.non_commit
		frappe.db.begin()
	

	def tearDown(self):
		frappe.db.rollback()

	def test_create_new_honorarium(self):
		honorarium = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("Medical Honorarium", frappe.db.get_value(model, {"name": honorarium["name"]}))
		self.assertEqual(doc.name, honorarium["name"])
