var MenuItem = Backbone.Model.extend({});


var MenuItemCollection = Backbone.Collection.extend({

    model: MenuItem,

    url: function() {
	// Only list the MenuItems which are descendants of the
	// MenuItem which is being edited.
	var base_url = "/admin/menus/menuitem/api/menuitems/";
	model_id = $("#menuitems").attr("data-root-menuitem-id" || null);
	console.log('model id', model_id);
	if (model_id != null) {
	    return base_url + "?root=" + model_id;
	};

	return base_url;
    }

});


var MenuItemView = Backbone.View.extend({

    tagName: 'li',
    template: _.template($("#menuitem-template").html()),

    render: function() {
	var ul = $("#menuitems");
	var li = $(this.el).html(this.template(this.model.toJSON()));
	ul.append(li);
	return this;
    },
});


var MenuItemsView = Backbone.View.extend({

    tagName: 'ul',

    render: function() {
	var menuitems = new MenuItemCollection();
	menuitems.fetch({async: false});

	menuitems.forEach(function(menuitem) {
	    var itemView = new MenuItemView({model: menuitem});
	    itemView.render();
	    $(this.el).append(itemView.render().el);
	});
    }
});


$(document).ready(function() {
    var itemsview = new MenuItemsView();
    itemsview.render();
});
