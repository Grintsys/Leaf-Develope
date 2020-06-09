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
		this.state = {};
		const assets = [
			'assets/erpnext/js/pos/clusterize.js',
			'assets/erpnext/css/point_of_sales.css'
		];
		this.get_pos_config()
		frappe.require(assets, () => {
			this.make();
		});
	}

	get_pos_config(){
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_pos_config",
			callback: function (item) {
			}
		})
	}

	make() {
		return frappe.run_serially([
			// ()=> frappe.dom.freeze(),
			() => {
				this.prepare_dom();
				this.prepare_menu();
				this.make_cart();

				//item-container
				this.detail();
				this.make_buttons();
				this.make_fields_detail_sale();
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

	make_cart() {
		var me = this;
		this.cart = new Cart({
			frm: this.frm,
			wrapper: this.wrapper.find('.cart-container'),
			events: {
				onClickAdd: (item) => {
					if(this.customer_field.get_value()){
						this.add_item(item);
						this.cart.search_field.set_value("");
						return;
					}
					frappe.throw(`${__('Customer is required')}`);
				},
				onChangeQuantity: (item_code,quantity)=>{
					this.update_item_quantity(item_code,quantity)
				},
				onChangeDiscount: (item_code,discount)=>{
					this.update_item_discount(item_code,discount)
				},
				onUpdatetotal:() => {
					this.update_totals();
				}

			}
		});
	}

	update_item_quantity(item_code,quantity){
		const itemRate = this.get_item_rate(item_code);
		const discount = Number(this.wrapper.find(`.${item_code}_discount`).val());
		this.wrapper.find(`.${item_code}_quantity`).val(quantity);
		const total = this.get_item_new_total(itemRate,discount,quantity);
		this.wrapper.find(`.${item_code}_total`).text(total);
	}

	
	get_item_max_discount(item_code){
		const item = $(this.wrapper.find(`div[data-item-code="${unescape(item_code)}"]`));
		return Number(item.attr('max_discount'));
	}


	update_item_discount(item_code,discount){
		const maxDiscount = this.get_item_max_discount(item_code);
		if(discount>maxDiscount){
		this.wrapper.find(`.${item_code}_discount`).val(0);
		discount = 0;
		frappe.msgprint(__("The discount exceeds the maximum limit"))
		}
		const itemRate = this.get_item_rate(item_code);
		const quantity = Number(this.wrapper.find(`.${item_code}_quantity`).val());
		this.wrapper.find(`.${item_code}_discount`).val(discount);
		const newTotal = this.get_item_new_total(itemRate,discount,quantity)
		this.wrapper.find(`.${item_code}_total`).text(newTotal);
	}

	get_item_new_total(itemRate,discount,quantity) {
		let discountRate = itemRate;
		if(discount > 0) discountRate = (itemRate) - ((discount/100) * itemRate)
		return (discountRate * quantity).toFixed(2);
	}

	update_totals(){
		let grandTotal = 0;
		let totalDiscount = 0;
		
		this.wrapper.find('.list-item').each((index,item)=>{
			grandTotal += Number($(item).find('.total').text());
			totalDiscount += this.get_item_total_discount(item);
		});
		this.wrapper.find('.grand-total-value').text(grandTotal.toFixed(2));
		this.wrapper.find('.total-discount-value').text(totalDiscount.toFixed(2));
	}

	get_item_total_discount(item){
		const itemRate = Number($(item).find('.rate').text());
		const itemDiscount = Number($(item).find('.item_discount').val());
		const itemquantity = Number($(item).find('.item_quantity').val());
		return (itemRate * itemquantity) * (itemDiscount/100) || 0;
	}

	get_item_rate(item_code){
		return Number(this.wrapper.find(`.${item_code}_rate`).text());
	}

	check_repeated_items(item) {
		return this.wrapper.find(`[data-item-code="${escape(item)}"]`).length > 0 ? true : false;
	}

	add_item(item){	
		if(!item)return;
		if(this.check_repeated_items(item)){
			frappe.msgprint(__('Product already exists in list'))
			return;
		}
		const me = this;
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.item",
			args: {
				item: item
			},
			callback: function (item) {
				me.wrapper.find('.cart-items').append(get_item_html(item.message));
				me.update_totals();
				set_item_max_discount(item.message.item_code)
			}
		})

	function set_item_max_discount(code) {
			frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_item_max_discount",
			args: {
				item_code: code
			},
			callback: function (itemDiscount) {
				const item = $(me.wrapper.find(`div[data-item-code="${unescape(code)}"]`));
				item.attr('max_discount',itemDiscount.message);
			}
		})
	}


	function get_item_html(item) {
		return `
		<div class="list-item indicator green register"
		data-item-code="${escape(item.item_code)}"
		>
				<div class="item-name list-item__content list-item__content--flex-1.5">
				` + item.item_name + `
				</div>
				<div class="quantity list-item__content text-right ">
					${get_quantity_html(item)}
				</div>
				<div class="discount-percentage list-item__content text-muted text-right">
					${get_discount_html(item)}
				</div>
				<div class="rate list-item__content text-muted text-right ${item.item_code}_rate"
				>
				` + item.price_cu + `
				</div>
				<div class="total list-item__content text-muted text-right ${item.item_code}_total"
				>
				` + item.total + `
				</div>
				<div class="remove-icon list-item__content text-muted text-right">
					<i class="fa fa-trash red fa-lg btn trash-register"></i>
				</div>
			</div>
		`;
	}

	
	function get_quantity_html(item) {
		return `
			<div class="input-group input-group-xs input-number" >
		
				<input class="form-control item_quantity ${item.item_code}_quantity" type="number" min="1" value="1"/7>

			</div>
		`;
	}

	function get_discount_html(item) {
		return `
			<div class="input-group input-group-xs input-number">
				<input class="form-control item_discount ${item.item_code}_discount" type="number" min="0" value="0"/>
			</div>
		`;
	}
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
						<div class="customer_fields">
						</div>
					</div>
				<div>
			</div>
			</div>
			<div class="totals">
			</div>
			<div class="buttons flex">
			</div>
		`)
	}


	make_buttons() {
		this.wrapper.find('.buttons').append(`<div class="pause-btn" data-button-value="pause">Pause</div>`);
		this.wrapper.find('.buttons').append(`<div class="checkout-btn" data-button-value="checkout">Checkout</div>`);
	}

	make_rtn_field(selectedCustomer){
		const me = this;
		if(!selectedCustomer){
			return;
		}
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_customer_rtn",
			args: {
				customer_name: selectedCustomer
			},
			callback: function (customer) {
				me.wrapper.find('div[data-fieldname="customer_rtn"]').remove();
				if(customer.message.customer_default)return;
				me.customer_rtn_field = frappe.ui.form.make_control({
					df: {
						fieldtype: 'Data',
						label: __('RTN'),
						fieldname: 'customer_rtn',
						read_only: 1
					},
					parent: me.wrapper.find('.customer_fields'),
					render_input: true,
				});
				me.customer_rtn_field.set_value(customer.message.rtn)

			}
		})
		

	}

	make_fields_detail_sale(){
		const me = this;
		this.customer_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Customer'),
				fieldname: 'customer',
				options: 'Customer',
				reqd: 1,
				onchange:function() {
					me.make_rtn_field(me.customer_field.get_value());
				},
			},
			parent: this.wrapper.find('.customer_fields'),
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
		  
		  this.wrapper.find('.detail').append(`
			<div class="card">
				<div class="card-header" id="headingThree">
		  			<h2 class="mb-0">
						<button class="btn btn-link btn-block btn-collapse control-label" type="button" data-toggle="collapse" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
							<a>
			  					<i class="octicon octicon-chevron-down"></i>
			  						${__('Exempt and ISV')}
		  					</a>
						</button>
		  			</h2>
				</div>
				<div id="collapseThree" class="collapse" aria-labelledby="headingThree" data-parent="#accordionExample">
		  			<div class="card-body exempt_and_isv">
		  			</div>
				</div>
	  		</div>
	  	`);

		this.make_field_detail_discount();
		this.make_fields_total_detail();
		this.make_exempt_and_isv();
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

		this.payment_amount_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Payment amount'),
				fieldname: 'payment_amount'
			},
			parent: this.wrapper.find('.detail-payment'),
			render_input: true,
		});

		this.payment_card_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Payment credit card'),
				fieldname: 'payment_card',
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
		const me = this;
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

		this.type_margin_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Select',
				label: __('Margin type'),
				fieldname: 'margin_type',
				options: [
					'Percentage',
					'Amount'
				],
				onchange:function() {
					me.make_discount_type(me.type_margin_field.get_value());
				},
			},
			parent: this.wrapper.find('.discount-detail'),
			render_input: true,
		});
	}

	make_discount_type(margin_type){
		const me = this;
		if (margin_type == "Percentage"){
			me.wrapper.find('div[data-fieldname="amount"]').remove();
			this.percentage_for_discount_field = frappe.ui.form.make_control({
				df: {
					fieldtype: 'Int',
					label: __('Percentage for discount'),
					fieldname: 'percentage'
				},
				parent: this.wrapper.find('.discount-detail'),
				render_input: true,
			});
		}else{
			me.wrapper.find('div[data-fieldname="percentage"]').remove();
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
	}

	make_exempt_and_isv(){
		this.base_isv_15_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Base ISV 15'),
				fieldname: 'base_isv_15',
				read_only: 1
			},
			parent: this.wrapper.find('.exempt_and_isv'),
			render_input: true,
		});

		this.isv_15_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('ISV 15'),
				fieldname: 'isv_15',
				read_only: 1
			},
			parent: this.wrapper.find('.exempt_and_isv'),
			render_input: true,
		});

		this.base_isv_18_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Base ISV 18'),
				fieldname: 'base_isv_18',
				read_only: 1
			},
			parent: this.wrapper.find('.exempt_and_isv'),
			render_input: true,
		});

		this.isv_18_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('ISV 18'),
				fieldname: 'isv_18',
				read_only: 1
			},
			parent: this.wrapper.find('.exempt_and_isv'),
			render_input: true,
		});

		this.exempt_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Exempt'),
				fieldname: 'exempt',
				read_only: 1
			},
			parent: this.wrapper.find('.exempt_and_isv'),
			render_input: true,
		});

		this.exonerated_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Currency',
				label: __('Exonerated'),
				fieldname: 'exonerated',
				read_only: 1
			},
			parent: this.wrapper.find('.exempt_and_isv'),
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
						<div class="total-discount-value text-md text-dark-grey text-bold">0.00</div>
					</div>
				</div>
				<div class="grand-total flex justify-between items-center h-16 pr-8 pl-8 border-b-grey">
					<div class="flex flex-col">
						<div class="text-md text-dark-grey text-bold">Grand Total</div>
					</div>
					<div class="flex flex-col text-right">
						<div class="grand-total-value text-md text-dark-grey text-bold">0.00</div>
					</div>
				</div>
			</div>
		`);
	}
}



class Cart {
	constructor({frm, wrapper, events}) {
		this.frm = frm;
		this.item_data = {};
		this.wrapper = wrapper;
		this.events = events;
		this.make();
		this.bind_events();
	}

	make() {
		this.make_dom();
		this.make_fields();
	}

	make_dom() {
		this.wrapper.append(`
		<div class="pos-cart">
		<div class="fields">
			<div class="item-group-field">
			</div>
			<div class="search-field">
			</div>
			<div class="btn-add">
			</div>
		</div>
		<div class="cart-wrapper">
			<div class="list-item-table">
				<div class="list-item list-item--head">
					<div class="list-item__content list-item__content--flex-1.5 text-muted">${__('Name')}</div>
					<div class="list-item__content text-muted text-right">${__('Quantity')}</div>
					<div class="list-item__content text-muted text-right">${__('Discount')}</div>
					<div class="list-item__content text-muted text-right">${__('Rate')}</div>
					<div class="list-item__content text-muted text-right">${__('Total')}</div>
					<div class="list-item__content text-muted text-right">${__('Actions')}</div>
				</div>
			</div>
		</div>
		<div class="cart-items">
		
		</div>
	</div>
		`);
	}
	
	make_fields() {
		const me = this;
		this.search_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Search Item'),
				fieldname: 'search_item',
				options: 'Item',
				placeholder: __('Search item by name, code and barcode'),
				get_query: () => {
					if (this.item_group_field.get_value() != 'Todos los Grupos de Artículos'){
						return {
							filters: {
								item_group: this.item_group_field.get_value()
							}
						};
					}
				}
			},
			parent: this.wrapper.find('.search-field'),
			render_input: true,
			
			
		});

		

		this.wrapper.find('.btn-add').append(`<button class="btn btn-default btn-xs add" data-fieldtype="Button">${__('Agregar')}</button>`);
		
		frappe.db.get_value("Item Group", {lft: 1, is_group: 1}, "name", (r) => {
			this.item_group_field.set_value(r.name);
		})
		
		this.item_group_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: 'Item Group',
				options: 'Item Group',
				fieldname: 'item_group'
			},
			parent: this.wrapper.find('.item-group-field'),
			render_input: true
		});
	}



	bind_events() {	
		var me = this;
		const events = this.events;
		this.wrapper.on('click', '.btn-add', function() {
			events.onClickAdd(me.search_field.get_value());
		});

		this.wrapper.on('change', '.item_quantity', function() {
			const $btn = $(this);
			const item = $btn.closest('.list-item[data-item-code]');
			const item_code = unescape(item.attr('data-item-code'));
			const quantity = Math.abs(Number(this.value));
			events.onChangeQuantity(item_code,quantity);
			events.onUpdatetotal();

		});

		this.wrapper.on('change', '.item_discount', function() {
			const $btn = $(this);
			const item = $btn.closest('.list-item[data-item-code]');
			const item_code = unescape(item.attr('data-item-code'));
			const discount = Math.abs(Number(this.value));
			events.onChangeDiscount(item_code,discount);
			events.onUpdatetotal();

		});
		this.wrapper.on('click', '.remove-icon', function() {
			const $btn = $(this);
			const item = $btn.closest('.list-item[data-item-code]');
			item.remove();
			events.onUpdatetotal();

		});
	}

}