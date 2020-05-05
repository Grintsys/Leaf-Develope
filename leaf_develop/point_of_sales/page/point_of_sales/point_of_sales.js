frappe.pages['point-of-sales'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Point of Sales',
		single_column: true
	});
	wrapper.point_of_sale = new erpnext.PointOfSales(wrapper);
}

erpnext.PointOfSales = class PointOfSales {
    constructor(wrapper) {
        var me = this;
        // 0 setTimeout hack - this gives time for canvas to get width and height
        setTimeout(function() {
            me.setup(wrapper);
        }, 0);
    }    setup(wrapper) {
        wrapper.page.add_action_icon(__("fa fa-trash text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });        wrapper.page.add_action_icon(__("fa fa-print text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });        wrapper.page.add_action_icon(__("fa fa-calculator text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });        wrapper.page.add_action_icon(__("fa fa-exchange text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });        wrapper.page.add_action_icon(__("fa fa-cut text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });        wrapper.page.add_action_icon(__("fa fa-lock text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });        wrapper.page.add_action_icon(__("fa fa-history text-secondary fa-2x btn"), function () {
            frappe.msgprint("Message");
        });
    }}