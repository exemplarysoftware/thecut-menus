var MenuItem = Backbone.Model.extend({});


var MenuItemCollection = Backbone.Collection.extend({

    model: MenuItem,

    // initialize: function(models, options) {
    // 	delete this.paginationConfig;
    // 	this.paginationConfig = {
    // 	    pretty: false,
    // 	    ipp: 5,
    // 	    page_attr: 'page',
    // 	    ipp_attr: 'limit',
    // 	    fetchOptions: {'async': false, 'reset': true}
    // 	};

    url: "/admin/menus/menuitem/api/menuitems/"
	

});


var MenuItemView = Backbone.View.extend({

    tagName: 'li',
    template: _.template($("#menuitem-template").html()),

    render: function() {
	console.log('rendering MenuItemView');
	var ul = $("#menuitems");
	var li = $(this.el).html(this.template(this.model.toJSON()));
	ul.append(li);
	// console.log('inside menu item view');
	// console.log(this.model.get('name'));
	return this;
    },
});


var MenuItemsView = Backbone.View.extend({

    tagName: 'ul',

    render: function() {
	console.log('Rendering MenuItemsView');
	var menuitems = new MenuItemCollection();
	console.log('Fetching MenuItems');
	menuitems.fetch({async: false});
	console.log('Fetched ' + menuitems.length + ' MenuItems:');

	menuitems.forEach(function(menuitem) {
	    console.log('Creating MenuItemView');
//	    var el = $("#menuitems");
	    var itemView = new MenuItemView({model: menuitem});
	    console.log('rendering...');
	    itemView.render();
	    $(this.el).append(itemView.render().el);
	});

	console.log('Done rendering MenuItemsView');
    }
});


$(document).ready(function() {
    var itemsview = new MenuItemsView();
    itemsview.render();
});
