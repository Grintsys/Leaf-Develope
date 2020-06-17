# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class OpeningPOS(Document):
	@frappe.whitelist()
	def validate(self):
		user = frappe.session.user
		pos = frappe.get_value('GCAI Allocation',{"user":user},["pos","branch"],as_dict =1)


		openings = frappe.get_all("Opening POS",["*"],filters = {"cashier": pos.pos,"branch":pos.branch},order_by = "creation desc") 
		lastOpening = next(iter(openings),None)
		clousures = frappe.get_all("Close Pos",["*"],filters = {"pos": pos.pos,"sucursal":pos.branch},order_by = "creation desc") 
		lastClousure = next(iter(clousures),None)
		if lastOpening is None:
			return

		if lastClousure is None:
			frappe.throw(_("There is an active opening for this POS and Branch"))
		elif lastOpening.creation > lastClousure.creation:			
			frappe.throw(_("There is an active opening for this POS and Branch"))
		


