describe('MenuItem Model', function() {

    it('should set its defaults', function() {
	var menuItem = new MenuItem();

	expect(menuItem).to.be.ok;
	expect(menuItem.get('id')).to.equal(null);
	expect(menuItem.get('name')).to.equal('');
	expect(menuItem.get('parent')).to.equal(null);
	expect(menuItem.get('content_type')).to.equal(null);
	expect(menuItem.get('object_id')).to.equal(null);
    });

    it('should include its ID in its URL', function() {
	var menuItem = new MenuItem({id: '123'});
	var url = menuItem.url(); 

	expect(url).to.contain('123'); // Why the TypeError?
    });

    it('should have an empty menu item collection', function() {
	var menuItem = new MenuItem();

	expect(menuItem.children).to.be.ok;
	expect(menuItem.children.length).to.equal(0);
    });

});
