# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

# import frappe
import unittest

class TestInventoryRequisition(unittest.TestCase):
	def setUp(self):
		data(setup=True)

def data(setup=False, test_tax=False):
	data = [
		{
			"patient_statement": 'Prueba',
			"date_create":'10-02-2020 15:34:04',
			"products": [{
				"item": 'CLI-SER-0003',
				"product_name": 'Colchon de agua',
				"quantity": 2
			}],
			"state": 'Open'
		}
	]
	return data