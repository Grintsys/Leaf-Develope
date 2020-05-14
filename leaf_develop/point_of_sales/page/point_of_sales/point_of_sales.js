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
			'assets/erpnext/css/point_of_sales.css'
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
				this.item_list();
				this.detail();
				this.make_buttons();
				this.make_fields();
				this.make_fields_detail_sale();
				this.click_add();
				// this.make_table_items();
			},
			() => this.page.set_title(__('Point of Sales'))
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
			
		});
		this.page.add_action_icon(__("fa fa-print text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-calculator text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
		this.page.add_action_icon(__("fa fa-exchange text-secondary fa-2x btn"), function () {
			frappe.route_options = {"sucursal": "Principal", "pos": "Caja01"}
			frappe.new_doc("Withdrawal and Entry")
		});
		this.page.add_action_icon(__("fa fa-cut text-secondary fa-2x btn"), function () {
			frappe.route_options = {"sucursal": "Principal", "pos": "Caja01"}
			frappe.new_doc("Point of sale Cut")
		});
		this.page.add_action_icon(__("fa fa-lock text-secondary fa-2x btn"), function () {
			frappe.route_options = {"sucursal": "Principal", "pos": "Caja01"}
			frappe.new_doc("Close Pos")
		});
		this.page.add_action_icon(__("fa fa-history text-secondary fa-2x btn"), function () {
			frappe.msgprint("Message");
		});
	}

	click_add(){		
		this.wrapper.find('.add').on('click', () => {			
			this.add_item();
		})
	}

	add_item(){	
		
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.item",
			args: {
				item: this.search_field.get_value()
			},
			callback: function (r) {
				localStorage.setItem("r", Object.values(r))		
			}
		})

		var data = localStorage.getItem("r");

		var arr = data.split(",");

		this.wrapper.find('.tbody-items').append(`
			<tr>
			<th scope="row">` + arr[0] + `</th>
			<td><input type="number" value="1"></td>
			<td><input type="currency" value="0"></td>
			<td>` + arr[1] + `</td>
			<td>` + arr[2] + `</td>
			</tr>
		`)
	}

	item_list(){
		this.wrapper.find('.cart-container').append(`
			<div class="pos-cart">
				<div class="fields">
					<div class="item-group-field">
					</div>
					<div class="search-field">
					</div>
					<div class="btn-add">
					</div>
					<div class="items-wrapper">
					</div>
				</div>
				<div class="cart-wrapper">
					
				</div>
				<div class="cart-items">
				
				</div>
			</div>
		`)
	}

	detail(){
		this.wrapper.find('.item-container').append(`
			<div class="pos-cart">
				<div class="cart-wrapper">
					<div class="list-item-table list-item list-item--head">
						<h5 class="text-muted">Detail of sale</h5>
					</div>
				</div>
				<div class="detail-items">
					<div class="detail">
					</div>
					<div class="totals">
					</div>
				<div>
			</div>
			</div>
			<div class="buttons flex">
			</div>
		`)
	}


	make_fields() {
		// Search field
		const me = this;
		this.search_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Search Item'),
				fieldname: 'search_item',
				options: 'Item',
				placeholder: __('Search item by name, code and barcode')
			},
			parent: this.wrapper.find('.search-field'),
			render_input: true,
		});

		this.wrapper.find('.btn-add').append(`<button class="btn btn-default btn-xs add" data-fieldtype="Button">Agregar</button>`);

		this.item_group_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: 'Item Group',
				options: 'Item Group',
			},
			parent: this.wrapper.find('.item-group-field'),
			render_input: true
		});
	}

	make_buttons() {
		this.wrapper.find('.buttons').append(`<div class="pause-btn" data-button-value="pause">Pause</div>`);
		this.wrapper.find('.buttons').append(`<div class="checkout-btn" data-button-value="checkout">Checkout</div>`);
	}

	make_table_items(){
		this.table_items = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Table',
				label: __(''),
				fieldname: 'pos_table_item',
				options: 'Pos Table Item',
			},
			parent: this.wrapper.find('.cart-items'),
			render_input: true,
		});
	}

	make_fields_detail_sale(){
		const me = this;
		this.customer_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Customer'),
				fieldname: 'customer',
				options: 'Customer',
				reqd: 1
			},
			parent: this.wrapper.find('.detail'),
			render_input: true,
		});

		this.numeration_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Data',
				label: __('Numeration'),
				fieldname: 'numeration',
				read_only: 1
			},
			parent: this.wrapper.find('.detail'),
			render_input: true,
		});

		this.wrapper.find('.detail').append(`
			<div class="accordion" id="accordionExample">
				<div class="card">
		  			<div class="card-header" id="headingOne">
						<h2 class="mb-0">
			  				<button class="btn btn-link btn-block btn-collapse control-label" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
			  					<a>
									<i class="octicon octicon-chevron-down"></i>
			  							${__('Detail of discount')}
		  						</a>
			  				</button>
						</h2>
		  			</div>
		  			<div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
						<div class="card-body discount-detail">
						</div>
		  			</div>
				</div>
			</div>
		`);
		
		this.wrapper.find('.detail').append(`
			<div class="card">
				<div class="card-header" id="headingTwo">
		  			<h2 class="mb-0">
						<button class="btn btn-link btn-block btn-collapse control-label" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
							<a>
			  					<i class="octicon octicon-chevron-down"></i>
			  						${__('Detail of payment')}
		  					</a>
						</button>
		  			</h2>
				</div>
				<div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionExample">
		  			<div class="card-body detail-payment">
		  			</div>
				</div>
	  		</div>
	  	`);

		this.make_field_detail_discount();
		this.make_fields_total_detail();
		this.make_totals();
	}

	make_fields_total_detail(){
		this.reason_for_sale_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Reason for sale'),
				fieldname: 'reason_for_sale',
				options: 'Reason for sale'
			},
			parent: this.wrapper.find('.detail-payment'),
			render_input: true,
		});

		this.exonerated_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Check',
				label: __('Exonerated Sale'),
				fieldname: 'exonerated'
			},
			parent: this.wrapper.find('.detail-payment'),
			render_input: true,
		});

		this.return_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Return'),
				fieldname: 'return'
			},
			parent: this.wrapper.find('.detail-payment'),
			render_input: true,
		});
	}

	make_field_detail_discount(){
		this.reason_for_discount_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Discount reason'),
				fieldname: 'discount_reason',
				options: 'Reason For Discount'
			},
			parent: this.wrapper.find('.discount-detail'),
			render_input: true,
		});

		this.percentage_for_discount_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Int',
				label: __('Percentage for discount'),
				fieldname: 'percentage'
			},
			parent: this.wrapper.find('.discount-detail'),
			render_input: true,
		});

		this.amount_for_discount_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Amount for discount'),
				fieldname: 'amount'
			},
			parent: this.wrapper.find('.discount-detail'),
			render_input: true,
		});
	}

	make_totals(){
		this.wrapper.find('.totals').append(`
			<div class="border border-grey fixed-bottom">
				<div class="total-discount flex justify-between items-center h-16 pr-8 pl-8 border-b-grey">
					<div class="flex flex-col">
						<div class="text-md text-dark-grey text-bold">Discount</div>
					</div>
					<div class="flex flex-col text-right">
						<div class="text-md text-dark-grey text-bold">0.00</div>
					</div>
				</div>
				<div class="grand-total flex justify-between items-center h-16 pr-8 pl-8 border-b-grey">
					<div class="flex flex-col">
						<div class="text-md text-dark-grey text-bold">Grand Total</div>
					</div>
					<div class="flex flex-col text-right">
						<div class="text-md text-dark-grey text-bold">0.00</div>
					</div>
				</div>
			</div>
		`);
	}

}