context('ReturnOfInvetoryRequisition', () => {
    before(() => {
		cy.visit('http://localhost:8000/login#login');
	});

	it('Create a new return of inventory requisition', () => {
		cy.get('#login_email').type('Administrator', { delay: 200});
		cy.get('#login_password').type('Admin.123', { delay: 200});
		cy.get('.btn-login').click();
		cy.get('[href="#modules/Account status"]').click({ force: true});
		cy.get('[href="#List/Return of inventory requisition"]').click({ force: true});
		cy.get('[data-label="Nuevo"]').click({ force: true});
		cy.get('input[data-fieldname="patient_statement"]').last().click({multiple: true, force: true});
		cy.get('input[data-fieldname="patient_statement"]').last().type('New');
		cy.get('input[data-fieldname="date_create"]').first().click();
		cy.wait(4000);
        cy.get('input[data-fieldname="date_create"]').last().type('09-03-2020');
        cy.get('[data-fieldname="products"]').click({multiple: true, force: true});
        cy.get('[data-fieldname="item"]').click({multiple: true, force: true});
        cy.wait(4000);
        cy.contains('P0001').click({force: true})
        cy.get('[data-fieldname="quantity"]').first().click();
        cy.get('[data-fieldname="quantity"]').last().type('5');
        cy.contains('Guardar').click({ force: true });
	});
});