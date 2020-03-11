# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import frappe.defaults
import unittest

test_records = frappe.get_test_records('GSucursal')
model = "GSucursal"

def default_data():
	return {
	    "doctype":"GSucursal",
		"name": "Central",
		"company": "Diagnóstico Medico Digital - DIMEDI",
		"code": "001"
	}

def create_events():

	if frappe.flags.test_events_created:
		return
		
	register = default_data()
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
		"doctype": register["doctype"],
		"name": register["name"],
		"company": register["company"],
		"code": register["code"]
    }).insert()

	frappe.flags.test_events_created = True

class TestGSucursal(unittest.TestCase):
	def setUp(self):
		create_events()
	
	def test_create_register_TRUE(self):
		register = default_data()
		frappe.set_user("Administrator")
		doc = frappe.get_doc("GSucursal", frappe.db.get_value("GSucursal",{"code": register["code"]}))
		self.assertEquals(doc.code,"001")
