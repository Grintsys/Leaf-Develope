# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document

class Medical(Document):
	def validate(self):
		name = self.first_name + " " + self.last_name
		self.full_name = name