describe('MenuItem Model', function() {

    it('should set its defaults which are not rendered to null', function() {
	var menuItem = new MenuItem();

	expect(menuItem).to.be.ok;
	expect(menuItem.get('id')).to.equal(null);
	expect(menuItem.get('parent')).to.equal(null);

    });

    it('should set its defaults which are rendered to renderable values', function() {
	var menuItem = new MenuItem();

	expect(menuItem.get('name')).to.equal('');
	expect(menuItem.get('content_type')).to.equal('');
	expect(menuItem.get('content_object')).to.equal('');
	expect(menuItem.get('object_id')).to.equal('');
	expect(menuItem.get('is_menu')).to.equal(false);
    });

    it('should include its ID in its URL', function() {
	var menuItem = new MenuItem({id: '123'});
	var url = menuItem.url(); 

	expect(url).to.contain('123'); // Why the TypeError?
    });

});


describe('MenuItem View', function() {

    before(function() {
	// Create a test fixture.
	this.$fixture = $('<div id="menuitem-view-fixture"></div>');
    });

    beforeEach(function() {
	// Clear out the fixture before each run.
	this.$fixture.empty().appendTo($('#fixtures'));
	this.view = new MenuItemView({el: this.$fixture,
				      model: new MenuItem({id: 1})});
	this.view.render();
    });

    afterEach(function() {
	// Destroying the model also destroys the view.
	this.view.model.destroy();
    });

    after(function() {
	// Remove everything from the fixtures element.
	$('#fixtures').empty();
    });

    it('should set its attributes based on its model\'s id ', function() {
	var attributes = this.view.attributes();

	expect(attributes).to.include.keys('data-pk');
	expect(attributes['data-pk']).to.equal(1);
	expect(attributes).to.include.keys('data-sortable-pk');
	expect(attributes['data-sortable-pk']).to.equal('pk_1');
    });

});
