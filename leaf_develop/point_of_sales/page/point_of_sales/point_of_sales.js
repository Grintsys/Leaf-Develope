frappe.pages['point-of-sales'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Point of Sales',
		single_column: true
	});

	page.set_indicator('Online', 'green')

	frappe.call({
		method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_pos_config",
		callback: function (item) {
			if(item){
					wrapper.point_of_sale = new erpnext.PointOfSales(wrapper,item.message);
				return;
			}
			frappe.throw("no config")
		}
	})
}


frappe.pages['point-of-sales'].on_page_show = function(wrapper){
	frappe.call({
		method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_pos_config",
		callback: function (item) {
				if(item.message.requiresOpening)
					frappe.new_doc("Opening POS")
		}
	})

}





erpnext.PointOfSales = class PointOfSales {
	constructor(wrapper,config) {
		// 0 setTimeout hack - this gives time for canvas to get width and height
		this.wrapper = $(wrapper).find('.layout-main-section');
		this.page = wrapper.page;
		this.config = config;
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
			// ()=> frappe.dom.freeze(),
			()=>{
				this.prepare_dom();
				this.prepare_menu();
				this.make_cart();
				this.make_detail();
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

	print_invoice(){
		debugger
	}

	clear_invoice(){
		$(this.wrapper.find('.item-list-cart')).remove();
		this.update_totals();
		this.customer_field.set_value("");
		this.wrapper.find('div[data-fieldname="customer_rtn"]').remove();
	}

	open_modal_auth(callback){
		const me = this;
		var dialog = new frappe.ui.Dialog({
			title:__('Authentication'),
			fields: [
				{fieldname: 'password', fieldtype: 'Password',label:`Password`},
			],
			primary_action: (values) => {
				if(values.password === me.config.credential){
					callback();
					dialog.hide();
					return;
				}
				dialog.wrapper.find('input[data-fieldname="password"]').val("")
				frappe.throw("Unauthorized credential")
			}
		});

		dialog.show();
		
	}

	make_cut(){
		frappe.route_options = {"sucursal": "Principal", "pos": "Caja01"}
		frappe.new_doc("Point of sale Cut")
	}

	prepare_menu() {
		const me = this;

		this.page.add_action_icon(__("fa fa-trash text-secondary fa-2x btn"), function () {
			if(me.config.clear_all_screen_items){
				me.clear_invoice(me);
				return;
			}
			me.open_modal_auth(()=> {
				me.clear_invoice();
			});

		});

		this.page.add_action_icon(__("fa fa-print text-secondary fa-2x btn"), function () {
			if(me.config.authorize_reprint_invoice){
				me.print_invoice();
				return
			}
			me.open_modal_auth(()=> {
				me.print_invoice();
			});
		});

		this.page.add_action_icon(__("fa fa-calculator text-secondary fa-2x btn"), function () {
			
		});
		this.page.add_action_icon(__("fa fa-exchange text-secondary fa-2x btn"), function () {
			frappe.route_options = {"sucursal": "Principal", "pos": "Caja01"}
			frappe.new_doc("Withdrawal and Entry")
		});
		this.page.add_action_icon(__("fa fa-cut text-secondary fa-2x btn"), function () {
			if(me.config.make_cut){
				me.make_cut();
				return;
			}
			me.open_modal_auth(() =>me.make_cut());
			
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
					if(this.detail.customer_field.get_value()){
						this.add_item(item);
						// this.cart.search_field.set_value("");
						$(this.wrapper.find('input[data-fieldname="search_item"]')).val("")
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
				onChangeRate:(item_code,rate)=>{
					this.update_item_rate(item_code,rate)
				},
				onUpdatetotal:() => {
					this.update_totals();
				},
				onRemoveItem: (item) => {
					if(this.config.delete_an_invoice_item){
						item.remove();
						this.update_totals();
						return;
					}
					this.open_modal_auth(()=> {
						item.remove();
						this.update_totals();
					})
				}

			},
			config: this.config
		});
	}

	get_max_discount_amount_config() {
		let grandTotal = 0;
		this.cart.wrapper.find('.list-item').each((index,item)=>{
			grandTotal += Number($(item).find('.total').text());
		});
		return grandTotal * (this.config.max_discount_percentage/100);
	}

	updatePercentageDiscount(discount){
		$(this.wrapper.find('input[data-fieldname="percentage"]')).val(discount);
		this.update_totals()
	}

	updateAmountDiscount(discount){
		$(this.wrapper.find('input[data-fieldname="amount"]')).val(discount);
		this.update_totals()
	}

	proceed_checkout(){
		let invoice_data= {
			customer: this.detail.customer_field.get_value()
		}
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.proceed_checkout",
			args: {
				invoice_data
			},
			callback: function (item) {
			debugger
			}
		})


	}

	make_detail() {
		var me = this;
		this.detail = new Detail({
			frm: this.frm,
			wrapper: this.wrapper.find('.item-container'),
			events: {
				onClickCheckout:()=>{
					me.proceed_checkout()
				},
				onChangePercentageDiscount(discount){
					if(discount <= me.config.max_discount_percentage){
						me.updatePercentageDiscount(discount)
						return
					}
					if(me.config.allow_override_max_discount){
						me.open_modal_auth(()=> 
						me.updatePercentageDiscount(discount)
						);
					}
					else{
						frappe.msgprint(`Discount is greather than ${me.config.max_discount_percentage}%`)
					}	
					$(me.wrapper.find('input[data-fieldname="percentage"]')).val(0);
					me.update_totals()
				},
				onChangeAmountDiscount(discount){
					const maxAmount = me.get_max_discount_amount_config(); 
					if(discount <= maxAmount){
						me.updateAmountDiscount(discount)
						return
					}
					if(me.config.allow_override_max_discount){
						me.open_modal_auth(()=> me.updateAmountDiscount(discount));
					}
					else{
						frappe.msgprint(`Discount is greather than ${maxAmount.toFixed(2)}`)
					}
					$(me.wrapper.find('input[data-fieldname="amount"]')).val(0);
					me.update_totals()
				}
			},
			config: this.config
		});
	}


	update_item_quantity(item_code,quantity){
		const itemRate = this.get_item_rate(item_code);
		const discount = Number(this.wrapper.find(`.${item_code}_discount`).val());
		this.wrapper.find(`.${item_code}_quantity`).val(quantity);
		const total = this.get_item_new_total(itemRate,discount,quantity);
		this.wrapper.find(`.${item_code}_total`).text(total);
	}

	update_item_rate(item_code,itemRate){
		const discount = Number(this.wrapper.find(`.${item_code}_discount`).val());
		const quantity = Number(this.wrapper.find(`.${item_code}_quantity`).val());
		this.wrapper.find(`.${item_code}_rate`).val(itemRate.toFixed(2));
		const total = this.get_item_new_total(itemRate,discount,quantity);
		this.wrapper.find(`.${item_code}_total`).text(total);
	}
	
	get_item_max_discount(item_code){
		const item = $(this.wrapper.find(`div[data-item-code="${unescape(item_code)}"]`));
		return Number(item.attr('max_discount'));
	}


	update_item_discount(item_code,discount){
		const me = this;
		const maxDiscount = this.get_item_max_discount(item_code);
		if(discount>maxDiscount){
			this.wrapper.find(`.${item_code}_discount`).val(0);
			this.open_modal_auth(()=> {
				set_item_discount(item_code,discount)
				this.update_totals()

			});
		}
		else{
			set_item_discount(item_code,discount)
			this.update_totals()

		}		

		function set_item_discount(item_code,discount){
			const itemRate = me.get_item_rate(item_code);
			const quantity = Number(me.wrapper.find(`.${item_code}_quantity`).val());
			me.wrapper.find(`.${item_code}_discount`).val(discount);
			const newTotal = me.get_item_new_total(itemRate,discount,quantity)
			me.wrapper.find(`.${item_code}_total`).text(newTotal);
		}
	}

	get_item_new_total(itemRate,discount,quantity) {
		let discountRate = itemRate;
		if(discount > 0) discountRate = (itemRate) - ((discount/100) * itemRate)
		return (discountRate * quantity).toFixed(2);
	}

	update_totals(){
		let grandTotal = 0;
		let totalDiscount = 0;
		let totalISV15 = 0;
		let totalBase15 = 0;
		let totalBase18 = 0;
		let totalBase0 = 0;
		let totalISV18 = 0;


		
		this.wrapper.find('.list-item').each((index,item)=>{
			let itemPrice= Number($(item).find('.total').text());
			grandTotal += itemPrice;
			let closestitem = $(item).closest('.list-item[data-item-code]');
			let isv = Number(closestitem.attr('isv'));
			if(isv === 15){
				totalISV15 += this.get_item_isv(itemPrice,isv)
				totalBase15 += itemPrice;
			}
			if(isv === 18){
				totalISV18 += this.get_item_isv(itemPrice,isv)
				totalBase18 += itemPrice;
			}
			if(isv === 0){
				totalBase0 += itemPrice;
			}
			totalDiscount += this.get_item_total_discount(item);
		});
		const totalInvoiceDiscount = this.get_total_invoice_discount(grandTotal);
		totalDiscount += totalInvoiceDiscount;
		const discountDistroISV = totalInvoiceDiscount/grandTotal;
		grandTotal = this.get_total_invoice_value(grandTotal);
		this.detail.isv_15_field.set_value(this.get_discount_isv(discountDistroISV,totalISV15,totalBase15))
		this.detail.base_isv_15_field.set_value(this.get_discount_isv(discountDistroISV,totalISV15,0))
		this.detail.isv_18_field.set_value(this.get_discount_isv(discountDistroISV,totalISV18,totalBase18))
		this.detail.base_isv_18_field.set_value(this.get_discount_isv(discountDistroISV,totalISV18,0))
		this.detail.exempt_field.set_value(this.get_discount_isv(discountDistroISV,totalBase0,0))
		this.wrapper.find('.grand-total-value').text(grandTotal.toFixed(2));
		this.wrapper.find('.total-discount-value').text(totalDiscount.toFixed(2));
	}

	get_discount_isv(discount,isv,base){
		if(base === 0)
			return  isv - (discount * isv) || 0
		return (base - isv) - (discount * (base - isv)) || 0
	}

	get_item_isv(grandTotal,isv){
		return grandTotal / ((isv/100)+1)
	}

	get_total_invoice_value(grandTotal){
		let invoiceTotal= grandTotal;
		const percentage = $(this.wrapper.find('input[data-fieldname="percentage"]'));
		const amount = $(this.wrapper.find('input[data-fieldname="amount"]'));
		const selectedDiscount = this.detail.type_margin_field.get_value();
		
		if(selectedDiscount ==="Percentage"){
			if(percentage.length > 0)
				invoiceTotal -= grandTotal *(Number(percentage.val())/100)
			else invoiceTotal -= grandTotal *0
		}
		if(selectedDiscount ==="Amount"){
			if(amount.length > 0)
				invoiceTotal -= Number(amount.val())
			else invoiceTotal -=0
		}
		return invoiceTotal
	}

	get_total_invoice_discount(grandTotal){
		let invoiceDiscount = 0;
		const percentage = $(this.wrapper.find('input[data-fieldname="percentage"]'));
		const amount = $(this.wrapper.find('input[data-fieldname="amount"]'));
		const selectedDiscount = this.detail.type_margin_field.get_value();
		if(selectedDiscount ==="Percentage"){
			if(percentage.length > 0)
				invoiceDiscount+= grandTotal *(Number(percentage.val())/100)
			else invoiceDiscount+= grandTotal * 0
		}
		if(selectedDiscount ==="Amount"){
			if(amount.length > 0)
				invoiceDiscount += Number(amount.val())
			else invoiceDiscount += 0
		}
		return invoiceDiscount
	}

	get_item_total_discount(item){
		const itemRate = Number($(item).find('.item-rate').val());
		const itemDiscount = Number($(item).find('.item_discount').val());
		const itemquantity = Number($(item).find('.item_quantity').val());
		return (itemRate * itemquantity) * (itemDiscount/100) || 0;
	}

	get_item_rate(item_code){
		return Number(this.wrapper.find(`.${item_code}_rate`).val());
	}

	check_repeated_items(item) {
		return this.wrapper.find(`[data-item-code="${escape(item)}"]`).length > 0 ? true : false;
	}

	add_item(item){	
		if(!item)return;
		if(this.check_repeated_items(item)){
			const quantity = Number(this.wrapper.find(`.${item}_quantity`).val());
			this.update_item_quantity(item,quantity+1);
			this.update_totals();
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
		<div class="list-item item-list-cart indicator green register"
		data-item-code="${escape(item.item_code)}" isv="${item.isv}"
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
				<div class="rate list-item__content text-muted text-right">
				${get_rate_html(item)}
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

	function get_rate_html(item) {
		if(me.config.allow_user_to_edit_rate) return `
			<div class="input-group input-group-xs input-number">
				<input class="form-control  item-rate ${item.item_code}_rate" type="number" min="0" value="${item.price_cu}"/>
			</div>
		`;
		return `
		<div class="input-group input-group-xs input-number">
				<input class="form-control  item-rate ${item.item_code}_rate" type="number" min="0" disabled value="${item.price_cu}"/>
			</div>
		`
	}

	function get_discount_html(item) {
		if(me.config.allow_user_to_edit_discount) return `
			<div class="input-group input-group-xs input-number">
				<input class="form-control item_discount ${item.item_code}_discount "  type="number" min="0" value="0"/>
			</div>
		`;
		return `
		<div class="input-group input-group-xs input-number">
		<input class="form-control item_discount ${item.item_code}_discount "  disabled type="number" min="0" value="0"/>
			</div>
		`
		}
		}

	


}



class Cart {
	constructor({frm, wrapper, events,config}) {
		this.frm = frm;
		this.item_data = {};
		this.wrapper = wrapper;
		this.events = events;
		this.config = config;
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
		const allItemGroups = 'Todos los Grupos de Artículos'
		const me = this;
		this.search_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: __('Search Item'),
				fieldname: 'search_item',
				options: 'Item',
				placeholder: __('Search item by name, code and barcode'),
				get_query: () => {
					if (this.item_group_field.get_value() != allItemGroups){
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
		
		
		this.item_group_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: 'Item Group',
				options: 'Item Group',
				fieldname: 'item_group',
				get_query: () => {
						return {
						filters: [
								["Item Group","item_group_name","in",`${me.config.itemGroups.join()}`],
						]
						};
				}
			},
			parent: this.wrapper.find('.item-group-field'),
			render_input: true,
		
		});


		if(me.config.itemGroups.some((group) => group === allItemGroups)){
			this.item_group_field.set_value(allItemGroups);
		}
		if(me.config.itemGroups.length > 0){
			this.item_group_field.set_value(me.config.itemGroups[0]);
		}


	}



	bind_events() {	
		var me = this;
		const events = this.events;
		// this.wrapper.on('keyup', 'input[data-fieldname="search_item"]', function(e) {
		// 	if(e.keyCode === 13){
		// 		$(this).val()
		// 		setTimeout(()=>{
		// 			events.onClickAdd(me.scannerCode);
		// 		},200)
		// 		return
		// 	}
		// 	me.scannerCode = $(this).val()
		// });
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
		});

		this.wrapper.on('change', '.item-rate', function() {
			const $btn = $(this);
			const item = $btn.closest('.list-item[data-item-code]');
			const item_code = unescape(item.attr('data-item-code'));
			const rate = Math.abs(Number(this.value));
			events.onChangeRate(item_code,rate);
			events.onUpdatetotal();

		});

		this.wrapper.on('click', '.remove-icon', function() {
			const $btn = $(this);
			const item = $btn.closest('.list-item[data-item-code]');
			events.onRemoveItem(item);


		});
	}

}


























class Detail {
	constructor({frm, wrapper, events,config}) {
		this.frm = frm;
		this.item_data = {};
		this.wrapper = wrapper;
		this.events = events;
		this.config = config;
		this.make();
		this.bind_events();
	}

	make() {
		this.make_invoice_detail();
		this.make_buttons();
		this.make_fields_detail_sale();
	}


	bind_events() {	
		var me = this;
		const events = this.events;
		this.wrapper.on('click', '.checkout-btn', function() {
			events.onClickCheckout();
		});
		this.wrapper.on('change', 'input[data-fieldname="percentage"]', function(event) {
				var discountInput = $(this)
				events.onChangePercentageDiscount(Number(discountInput.val()));
			}
		)
		this.wrapper.on('change', 'input[data-fieldname="amount"]', function(event) {
			var discountInput = $(this)
			events.onChangeAmountDiscount(Number(discountInput.val()));
			}
		)
		this.wrapper.on('change', 'select[data-fieldname="margin_type"]', function(event) {
			events.onChangePercentageDiscount(0);
		}
		)	
	}

	make_buttons() {
		this.wrapper.find('.buttons').append(`<div class="pause-btn" data-button-value="pause">Pause</div>`);
		this.wrapper.find('.buttons').append(`<div class="checkout-btn" data-button-value="checkout">Checkout</div>`);
	}


	make_invoice_detail(){
		this.wrapper.append(`
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

	set_invoice_numeration(){
		const me = this;
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_invoice_numeration",
			args: {
			},
			callback: function (numeration) {
					me.numeration_field.set_value(numeration.message)
			}
		})
	}

	make_fields_detail_sale(){
		const allCustomerGroups = 'Todas las categorías de clientes'
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
				get_query: () => {
					let filters=[];
					if(me.config.customerGroup.some((group) => group === allCustomerGroups)){
						if(!me.config.allow_disabled_clients){
							filters.push( ["Customer","disabled","=",'0'])
							}
						return {filters};
					}
					filters.push(["Customer","customer_group","in",`${me.config.customerGroup.join()}`])

					if(!me.config.allow_disabled_clients)
						filters.push( ["Customer","disabled","=",'0'])

					return {filters};
				}
			},
			parent: this.wrapper.find('.customer_fields'),
			render_input: true,
		});

		this.customer_field.set_value(me.config.customer);
	

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

		this.set_invoice_numeration();

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

		this.get_discount_reasons();
		this.make_fields_total_detail();
		this.make_exempt_and_isv();
		this.make_totals();
	}

	make_payment_methods(){
		this.config.paymentMethods.forEach((i)=>{
			this[i] = frappe.ui.form.make_control({
				df: {
					fieldtype: 'Currency',
					label: __(i),
					fieldname: 'payment_amount'
				},
				parent: this.wrapper.find('.detail-payment'),
				render_input: true,
			});
			if(i =="Efectivo"){
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


		})

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

		this.make_payment_methods()
	}

	make_discount_fields(reasons) {
		const me = this;
		this.reason_for_discount_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Select',
				label: __('Discount reason'),
				fieldname: 'discount_reason',
				options: reasons
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

	get_discount_reasons(){
		const me = this;
		frappe.call({
			method: "leaf_develop.point_of_sales.page.point_of_sales.point_of_sales.get_margin_types",
			
			callback: function (marginTypes) {
				me.make_discount_fields(marginTypes.message)
			}
		})
		


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
