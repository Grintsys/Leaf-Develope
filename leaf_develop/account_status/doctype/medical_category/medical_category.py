# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document

class MedicalCategory(Document):
	def validate(self):
		self.verificate_new_category()
		
	def verificate_new_category(self):
		categories = frappe.get_all("Medical Category", ["rank"])
		for item in categories:
			if(item.rank == self.rank):
				frappe.throw(_("The category {} already exists".format(self.rank)))
