# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from leaf_develop.account_status.doctype.honorarium_payment.honorarium_payment import validate
import frappe.defaults
import unittest

test_records = frappe.get_test_records('Honorarium Payment')
model = "Honorarium Payment"

def default_data():
	return {
		"doctype":"Honorarium Payment",
		"honorarium": "AS-MH-2020-00019",
		"trasaction_date": "20-02-2020",
		"total": 20000
	}

def create_events():
	if frappe.flags.test_events_created:
		return

	payment = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": payment["doctype"],
		"honorarium": payment["honorarium"],
		"trasaction_date": payment["trasaction_date"],
		"total": payment["total"]
    }).insert()

	frappe.flags.test_events_created = True

class TestHonorariumPayment(unittest.TestCase):
	def setUp(self):
		create_events()

	def test_create_new_honorarium(self):
		payment = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("Honorarium Payment", frappe.db.get_value(model, {"honorarium": payment["honorarium"]}))
		self.assertEqual(doc.honorarium, payment["honorarium"])
