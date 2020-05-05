context('PatientStatement', () => {
    before(() => {
		cy.visit('http://localhost:8000/login#login');
	});

	it('Create a new patient statement', () => {
		cy.get('#login_email').type('Administrator', { delay: 200});
		cy.get('#login_password').type('Admin.123', { delay: 200});
		cy.get('.btn-login').click();
		cy.get('[href="#modules/Account status"]').click({ force: true});
		cy.get('[href="#List/Patient statement"]').click({ force: true});
		cy.get('[data-label="Nuevo"]').click({ force: true});
		cy.get('input[data-fieldname="__newname"]').last().click({multiple: true, force: true});
		cy.get('input[data-fieldname="__newname"]').last().type('New Patient');
		cy.get('input[data-fieldname="date"]').first().click();
		cy.wait(4000);
        cy.get('input[data-fieldname="date"]').last().type('09-03-2020');
		cy.get('input[data-fieldname="client"]').first().click({force: true});
		cy.wait(4000);
		cy.get('input[data-fieldname="client"]').last().type('German Roberto Guardiola', { delay: 200});
        cy.contains('Guardar').click({ force: true });
	});
});