context('HonorariumPayment', () => {
    before(() => {
		cy.visit('http://localhost:8000/login#login');
	});

	it('Create a new honorarium payment', () => {
		cy.get('#login_email').type('Administrator', { delay: 200});
		cy.get('#login_password').type('Admin.123', { delay: 200});
		cy.get('.btn-login').click();
		cy.contains('Estado de cuenta').click();
		cy.get('[href="#List/Honorarium Payment"]').click({ force: true});
		cy.get('[data-label="Nuevo"]').click({ force: true});
		cy.get('input[data-fieldname="honorarium"]').last().click({multiple: true, force: true});
		cy.get('input[data-fieldname="honorarium"]').last().type('AS-MH-2020-00018');
		cy.get('input[data-fieldname="transaction_date"]').first().click();
		cy.wait(4000);
        cy.get('input[data-fieldname="transaction_date"]').last().type('18-02-2020');
		cy.get('input[data-fieldname="total"]').first().click({force: true});
		cy.wait(4000);
		cy.get('input[data-fieldname="total"]').last().type('10000', { delay: 200});
        cy.contains('Guardar').click({ force: true });
	});
});