frappe.pages['point-of-sales'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Point of Sales',
		single_column: true
	});

	page.set_indicator('Online', 'green')

	wrapper.point_of_sale = new erpnext.PointOfSales(wrapper);
}

erpnext.PointOfSales = class PointOfSales {
	constructor(wrapper) {
		// 0 setTimeout hack - this gives time for canvas to get width and height
		this.wrapper = $(wrapper).find('.layout-main-section');
		this.page = wrapper.page;

		const assets = [
			'assets/erpnext/js/pos/clusterize.js',
			'assets/erpnext/css/pos.css'
		];

		frappe.require(assets, () => {
			this.make();
		});
	}

	make() {
		return frappe.run_serially([
			() => {
				this.prepare_dom();
				this.prepare_menu();
			},
			() => this.page.set_title(__('Point of Sale'))
		]);
	}

	prepare_dom() {
		this.wrapper.append(`
			<div class="pos">
				<section class="cart-container">

				</section>
				<section class="item-container">

				</section>
			</div>
		`);
	}

	prepare_menu() {
		this.page.add_action_icon(__("fa fa-trash text-secondary fa-2x btn"), function () {
			frappe.call({
				method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.item",
				args: {},
				callback: function (r) {

				}
			})
		});
		this.page.add_action_icon(__("fa fa-print text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-calculator text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-exchange text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-cut text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-lock text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-history text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
	}

}