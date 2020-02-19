context('MedicalHononoarium', () => {
    before(() => {
		cy.visit('http://localhost:8000/login#login');
	});

	it('Create a new honorarium', () => {
		cy.get('#login_email').type('Administrator');
		cy.get('#login_password').type('Admin.123');
		cy.get('.btn-login').click();
		cy.contains('Estado de cuenta').click();
		cy.get('[href="#List/Medical Honorarium"]').click({ force: true });
		cy.get('[data-label="Nuevo"]').click({ force: true});
		cy.get('[data-fieldname="medical"]').click({multiple: true});
		cy.get('[data-fieldname="medical"]').children().type('AS-MA-00001');
		cy.get('input[data-fieldname="total"]').first().click({force: true});
		cy.wait(4000);
		cy.get('input[data-fieldname="total"]').last().type('40000', { delay: 200});
		cy.get('input[data-fieldname="date"]').first().click({multiple: true});
		cy.wait(4000);
        cy.get('input[data-fieldname="date"]').last().type('18-02-2020');
        cy.contains('Guardar').click({ force: true });
	});
});