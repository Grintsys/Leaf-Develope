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
		"status": "Open",
		"company": "Servicios Medicos Multiples - Clínica",
		"date": "17-02-2020",
		"medical": "AS-MA-00001",
		"total": 20000
	}

def create_events():
	if frappe.flags.test_events_created:
		return

	honorarium = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": honorarium["doctype"],
		"status": honorarium["status"],
		"company": honorarium["company"],
		"date": honorarium["date"],
		"medical": honorarium["medical"],
		"total": honorarium["total"]
    }).insert()

	frappe.flags.test_events_created = True

class TestMedicalHonorarium(unittest.TestCase):
	def setUp(self):
		create_events()

	def test_create_new_honorarium(self):
		honorarium = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("Medical Honorarium", frappe.db.get_value(model, {"medical": honorarium["medical"]}))
		self.assertEqual(doc.medical, honorarium["medical"])

