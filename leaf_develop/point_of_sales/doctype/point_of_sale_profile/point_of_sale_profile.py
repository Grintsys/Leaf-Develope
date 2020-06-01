# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class PointOfSaleProfile(Document):
	def validate(self):
		cashier	= frappe.get_all("GPos", ["sucursal", "code", "sucursal"], filters={"name": self.cashier_name})
		for item in cashier:
			sucursal = frappe.get_all("GSucursal", "code", filters={"name": item.sucursal})
			for selected in sucursal:
				self.code_name = selected.code + "-" + item.code