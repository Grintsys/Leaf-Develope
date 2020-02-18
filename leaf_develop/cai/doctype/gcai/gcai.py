# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe.model.document import Document

class GCAI(Document):
		
    def validate(self):
        self.validate_range()
        self.validate_dates()
        self.validate_mask()
        self.generate_number()

    def on_trash(self):
        self.validate_delete()

    def validate_delete(self):
        sales_invoice = frappe.get_all("Sales Invoice", ["cai"], filters = {"cai": self.cai})

        if len(sales_invoice) != 0:
            frappe.throw(_("This CAI {} is associated with an invoice".format(sales_invoice[0].cai)))

    def validate_dates(self):
        if str(self.due_date) <= str(datetime.now()):
            frappe.throw(_("Date less than the current date."))

    def validate_range(self):
        if self.initial_range > self.final_range:
            frappe.throw(_("The initial range must be less than the final range"))
    
    def validate_mask(self):
        segment = 6

        for i in range(4):
            if self.cai[segment] != "-":
                frappe.throw(_("CAI: There is a problem with segment {}".format(i+1)))
            
            segment = segment + 7
        
        if len(self.cai) > 37:
            frappe.throw(_("CAI: There are more written characters"))

    def validate_cai(self):
        cais = frappe.get_all("GCAI", ["name"],filters = {"cai": self.cai})
        ranges_cais = frappe.get_all("GCAI", ["initial_range", "final_range", "due_date", "name"], filters = {"sucursal": self.sucursal, "pos_name": self.pos_name, "type_document": self.type_document})
        
        if len(cais) != 0:
            if cais[0].name != self.name:
                frappe.throw(_("This CAI exist."))

        for cai in ranges_cais:

            if self.initial_range >= cai.initial_range and self.initial_range <= cai.final_range and self.name != cai.name:
                frappe.throw(_("This initial range is using for other CAI."))
            
            if self.final_range >= cai.initial_range and self.final_range <= cai.final_range and self.name != cai.name:
                frappe.throw(_("This final range is using for other CAI."))

            if str(self.due_date) >= str(cai.due_date) and self.name != cai.name and self.final_range <= cai.initial_range:
                frappe.throw(_("The date cannot be greater than the date of the next CAI."))

    def validate_pos_and_sucursal(self, sucursal, sucursal_company, declaration_company):
        if sucursal_company != self.company:
            frappe.throw(_("This branch does not belong to this company"))
        
        if declaration_company != self.company:
            frappe.throw(_("This declaration does not belong to this company"))

        if sucursal != self.sucursal:
            frappe.throw(_("This pos does not belong to this branch"))
    
    def initial_number(self, num):

        if num >= 1 and num < 10:
            return("0000000" + str(num))
        elif num >= 10 and num < 100:
            return("000000" + str(num))
        elif num >= 100 and num < 1000:
            return("00000"+ str(num))
        elif num >= 1000 and num < 10000:
            return("0000" + str(num))
        elif num >= 10000 and num < 100000:
            return("000" + str(num))
        elif num >= 100000 and num < 1000000:
            return("00" + str(num))
        elif num >= 1000000 and num < 10000000:
            return("0" + str(num))
        elif num >= 10000000:
            return(str(num))
    
    def asing_state(self):
        cai = frappe.get_all("GCAI", ["name", "cai", "final_range"], filters = {"sucursal": self.sucursal, "pos_name": self.pos_name, "state": "Valid"})

        if len(cai) != 0 :
            if self.cai != cai[0].cai or int(self.current_numbering) == int(cai[0].final_range):
                return True
        
        return False
        

    def generate_number(self):
        self.validate_cai()

        document = frappe.get_all("GType Document",["number"],filters = {"name": self.type_document})
        sucursal= frappe.get_all("GSucursal",["code", "company"], filters = {"name": self.sucursal})
        pos = frappe.get_all("GPos",["code", "sucursal"], filters = {"name": self.pos_name})
        declaration = frappe.get_all("GNumber Declaration", ["no_declaration", "company"], filters = {"name": self.name_declaration})

        self.validate_pos_and_sucursal(pos[0].sucursal, sucursal[0].company, declaration[0].company)

        number = self.initial_number(self.initial_range)

        self.number = "{}-{}-{}-{}".format(sucursal[0].code, pos[0].code, document[0].number, number)

        self.no_declaration = "{}".format(declaration[0].no_declaration)
        
        self.state = "{}".format("Valid")
        
        if self.current_numbering is None:
            self.current_numbering = self.initial_range
        
        return True
