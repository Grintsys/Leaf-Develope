# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

test_records = frappe.get_test_records('GCai Settings')
model = "GCai Settings"

def default_data():
	return {
	    "doctype":"GCai Settings",
		"expired_days": 5,
		"expired_amount": 20
	}

def create_events():

	if frappe.flags.test_events_created:
		return
		
	register = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": register["doctype"],
		"expired_days": register["expired_days"],
		"expired_amount": register["expired_amount"]
    }).insert()

	frappe.flags.test_events_created = True

class TestGCaiSettings(unittest.TestCase):
	def setUp(self):
		create_events()
	
	def test_create_register_TRUE(self):
		register = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("GCai Settings", frappe.db.get_value("GCai Settings",{"expired_days": register["expired_days"]}))
		self.assertEquals(doc.expired_days,5)
