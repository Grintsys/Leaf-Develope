# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

test_records = frappe.get_test_records('Medical Category')
model = "Medical Category"

def default_data():
	return {
		'doctype': 'Medical Category',
		'specialty': 'Médico General'
	}
def create_events():
	if frappe.flags.test_events_created:
		return
	
	specialty = default_data()
	frappe.set_user("Administrator")

	doc = frappe.get_doc({
		"doctype": specialty["doctype"],
		"specialty": specialty["specialty"]
    }).insert()

	frappe.flags.test_events_created = True

class TestMedicalCategory(unittest.TestCase):
	def setUp(self):
		create_events()

	def test_create_new_medical_category(self):
		specialty = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("Medical Category", frappe.db.get_value("Medical Category",{"specialty": specialty["specialty"]}))
		self.assertEqual(doc.specialty, specialty["specialty"])

	def test_verificate_if_the_medical_category_is_non_recurring(self):
		specialty = default_data()
		specialty = specialty["specialty"]
		specialties = frappe.get_list(model, filters=[["Medical Category", "specialty", "like", specialty]], fields=["specialty"])
		self.assertEquals(len(specialties),1)
