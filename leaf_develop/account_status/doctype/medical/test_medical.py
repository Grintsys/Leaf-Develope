# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

test_records = frappe.get_test_records('Medical')
model = "Medical"

def default_data():
	return {
	    "doctype":"Medical",
		"first_name": "Izuku",
		"last_name": "Midoriya",
		"identification_card": "0501-0000-01768",
		"rtn": "0456-00H00",
		"rank": "Pediatra"
	}

def create_events():

	if frappe.flags.test_events_created:
		return
		
	doctor = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": doctor["doctype"],
		"first_name": doctor["first_name"],
		"last_name": doctor["last_name"],
		"identification_card": doctor["identification_card"],
		"rtn": doctor["rtn"],
		"rank": doctor["rank"]
    }).insert()

	frappe.flags.test_events_created = True

class TestMedical(unittest.TestCase):
	def setUp(self):
		create_events()

	def test_create_medical_by_administrator(self):
		doctor = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("Medical", frappe.db.get_value("Medical",{"first_name": doctor["first_name"]}))
		self.assertEqual(doc.full_name, doctor["first_name"] + ' ' + doctor["last_name"])
		
	def test_list_all_medical_records_by_administrator(self):
		frappe.set_user("Administrator")
		doctor = default_data()
		res = frappe.get_list(model, filters=[["Medical", "first_name", "like", "Izuku"]], fields=["full_name", "rtn"])
		self.assertEquals(len(res),1)