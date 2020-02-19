context('Medical', () => {
    before(() => {
		cy.visit('http://localhost:8000/login#login');
	});

	it('Create a new medical', () => {
		cy.get('#login_email').type('Administrator', { delay: 200});
		cy.get('#login_password').type('Admin.123', { delay: 200});
		cy.get('.btn-login').click();
    cy.contains('Estado de cuenta').click();
    cy.wait(4000);
    cy.get('[href="#List/Medical"]').click({ force: true,});
    cy.wait(4000);
        cy.get('[data-label="Nuevo"]').click({ force: true});
        cy.wait(4000);
        cy.get('[data-fieldname="first_name"]').click({multiple: true} );
        cy.get('[data-fieldname="first_name"]').children().type('Izuku', { delay: 200});
        cy.get('[data-fieldname="last_name"]').click({multiple: true} );
        cy.get('[data-fieldname="last_name"]').children().type('Midoriya', { delay: 200});
        cy.get('[data-fieldname="identification_card"]').click({multiple: true} );
        cy.get('[data-fieldname="identification_card"]').children().type('0501-1992-01768', { delay: 200});
        cy.get('[data-fieldname="rtn"]').click({multiple: true} );
        cy.get('[data-fieldname="rtn"]').children().type('0456-00H00', { delay: 200});
        cy.get('[data-fieldname="rank"]').click({multiple: true} );
        cy.get('[data-fieldname="rank"]').children().type('Pediatra', { delay: 200});
        cy.get('[data-fieldname="phone"]').click({multiple: true} );
        cy.get('[data-fieldname="phone"]').children().type('98492849', { delay: 200});
        cy.get('[data-fieldname="email"]').click({multiple: true} );
        cy.get('[data-fieldname="email"]').children().type('midoriya_izuku@leaf.com', { delay: 200});
        cy.get('[data-fieldname="current_address"]').click({multiple: true} );
        cy.get('[data-fieldname="current_address"]').children().type('San Pedro Sula, Cortés, Honduras', { delay: 200});
        cy.contains('Guardar').click({ force: true });
        cy.wait(4000);
        cy.get('[data-label="Validar"]').click({force: true})
        cy.get('button[class="btn btn-primary btn-sm"]').click({ force: true });
	});
});