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
		"date": "14-02-2020",
		"medical": "Izuku Midoriya",
		"total": 20000
	}

def create_events():
	if frappe.flags.test_events_created:
		return
	honorarium = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": honorarium["doctype"],
		"medical": honorarium["medical"],
		"total": honorarium["total"]
    }).insert()

	frappe.flags.test_events_created = True

class TestMedicalHonorarium(unittest.TestCase):
	def setUp(self):
		create_default_data()

	def test_create_new_honorarium(self):
		honorarium = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("Medical Honorarium", frappe.db.get_value(model, filters=[["name_medical", "like", honorarium["medical"]]]))
		self.assertEqual(doc.name_medical, honorarium["medical"])

