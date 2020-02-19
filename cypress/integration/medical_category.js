context('MedicalCategory', () => {
    before(() => {
		cy.visit('http://localhost:8000/login#login');
	});

	it('Create a new specialty', () => {
		cy.get('#login_email').type('Administrator');
		cy.get('#login_password').type('Admin.123');
		cy.get('.btn-login').click();
		cy.contains('Estado de cuenta').click();
		cy.get('[href="#List/Medical Category"]').click({ force: true });
        cy.get('[data-label="Nuevo"]').click({ force: true });
        cy.get('[data-fieldname="rank"]').click({multiple: true} );
        cy.get('[data-fieldname="rank"]').children().type('Cirujano');
        cy.contains('Guardar').click({ force: true });
	});
});