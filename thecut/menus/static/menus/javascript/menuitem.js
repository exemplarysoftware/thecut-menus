var MenuItem = Backbone.Model.extend({

    initialize: function() {
	this.children = new MenuItemCollection(this.id);
    },

    url: function() {
	return "/admin/menus/menuitem/api/menuitems/menuitem/" + this.id + "/";
    },

});


var MenuItemView = Backbone.View.extend({

    // HTML & CSS attributes.
    template: _.template($("#menuitem-template").html()),
    tagName: 'li',
    className: 'menuitem',

    attributes: function() {
	return {
	    'data-pk': this.model.get('id'),
	    'data-sortable-pk': 'pk_' + this.model.get('id'),
	};
    },

    events: {
	'click .edit.button': 'editClicked',
	'click .save.button': 'saveClicked',
	'click .delete.button': 'destroy',
	'change select.contenttype': 'updateContentType',
	'change select.contentobject': 'updateContentObject',
    },



    // Standard view functions.

    render: function() {
	// Render the contents of this single MenuItem.
	this.$el.html(this.template(this.model.toJSON()));

	// Insert any children this MenuItem might have.
	if ( this.model.get('is_menu') ) {
	    ul = $('<ul />', {'data-pk': this.model.get('id')});
	    this.children = new MenuItemCollectionView({
		'el': ul,
		'id': this.model.get('id')
	    });
	    this.children.render();
	    this.$el.append(ul);
	}
	return this;
    },

    save: function() {
	// Persist the changes made to the model.
	var nameValue = $(this.el).find("input.name").val().trim();
	this.model.save({name: nameValue});
    },

    destroy: function() {
	this.model.destroy();
    },


    // Custom functions.

    isEditable: function() {
	var saveButton = $(this.el).find("span.save.button");
	return saveButton.hasClass("enabled");
    },

    editClicked: function() {
	if ( !this.isEditable() ) {
	    // Put into editable state.
	    this.allowEditing();
	}
    },

    saveClicked: function () {
	if ( this.isEditable() ) {
	    this.preventEditing();
	    this.save();
	}
    },

    populateContentObjectSelect: function(contentTypes) {
	// Populate and enable the content object selector.
	var el = $(this.el).find("select.contentobject");

	// The <select> for choosing the content object, won't exist
	// if this is a sub-menu.
	if ( el !== null ) {
	    el.empty();
	    el.removeClass("disabled").addClass("enabled");
	    el.prop("disabled", false);
	    var contentType = new ContentType({id: this.model.get('content_type')});
	    contentType.fetch({async: false});
	    return contentType.getContentObjectSelect(el, this.model.get('object_id'));
	}
    },

    updateContentType: function() {
	// Update this item's content type and populate the content
	// object selector with items of the selected type.
	var el = $(this.el).find('select.contenttype');

	// The <select> for choosing the content type, won't exist if
	// this is a sub-menu.
	if ( el !== null ) {
	    this.model.set({content_type: el.val()});
	    var contentTypes = new ContentTypeCollection();
	    contentTypes.fetch({async: false});
	    this.populateContentObjectSelect(contentTypes);
	    this.updateContentObject();
	}
    },

    updateContentObject: function() {
	var select = $(this.el).find('select.contentobject');
	if ( select != null) {
	    this.model.set({object_id: parseInt(select.val(), 10)});
	}
    },

    allowEditing: function() {
	// Put the form into an editable state.

	// Make the 'name' field editable.
	var nameField = $(this.el).find("input.name");
	nameField.removeClass("disabled").addClass("enabled");
	nameField.prop("disabled", false);

	// Disable the 'Edit' button.
	var editButton = $(this.el).find(".edit.button");
	editButton.addClass("disabled").removeClass("enabled");

	// Enable the 'Save' button.
	var saveButton = $(this.el).find(".save.button");
	saveButton.removeClass("disabled").addClass("enabled");

	// Populate and enable the content type selector.
	var selector = $(this.el).find("select.contenttype");
	if ( selector != null )
	selector.empty(); {
	    var contentTypes = new ContentTypeCollection();
	    var active = this.model.get('content_type');
	    contentTypes.fetch({async: false});
	    contentTypes.populateContentTypeSelect(selector, active);
	    selector.removeClass("disabled").addClass("enabled");
	    selector.prop("disabled", false);
	    this.populateContentObjectSelect(contentTypes);
	}
    },

    preventEditing: function() {
	// Make the 'name' field non-editable.
	var nameField = $(this.el).find("input.name");
	nameField.addClass("disabled").removeClass("enabled");
	nameField.prop("disabled", true);

	// Enable the 'Edit' button.
	var editButton = $(this.el).find(".edit.button");
	editButton.removeClass("disabled").addClass("enabled");

	// Disable the 'Save' button.
	var saveButton = $(this.el).find(".save.button");
	saveButton.addClass("disabled").removeClass("enabled");

	// Disable the content type select.
	var contentTypeSelect = $(this.el).find("select.contenttype");
	contentTypeSelect.addClass("disabled").removeClass("enabled");
	contentTypeSelect.prop("disabled", true);

	// Disable the content object select.
	var contentObjectSelect = $(this.el).find("select.contentobject");
	contentObjectSelect.addClass("disabled").removeClass("enabled");
	contentObjectSelect.prop("disabled", true);
    },

});


var MenuItemCollection = Backbone.Collection.extend({

    model: MenuItem,

    initialize: function(parentId) {
	this.parentId = parentId;
    },

    url: function() {
	// Only the children of this collection's parent should be
	// included.
	var base_url = "/admin/menus/menuitem/api/menuitems/";
	return base_url + "?root=" + this.parentId;
    }

});


var MenuItemCollectionView = Backbone.View.extend({

    tagName: 'div',
    template: _.template($("#menu-template").html()),
    className: 'menu',

    initialize: function() {
	this.collection = new MenuItemCollection(this.id);
	this.collection.on('destroy', this.menuItemDestroyed, this);
    },

    render: function() {
	// Render the containing template.
	this.$el.html(this.template({id: this.id}));

	// Render the list of menu items inside this collection.
	var list = this.$el.find("ul.menu");
	this.collection.fetch({async: false});
	this.collection.each(function(menuitem) {
	    var itemView = new MenuItemView({model: menuitem});
	    list.append(itemView.render().el);
	}, this);

	return this;
    },

    menuItemDestroyed: function() {
	this.render();
    }

});


// The "application" view, which sets up and renders the initial
// content.
var MenuView = Backbone.View.extend({

    el: '#menu',

    render: function() {
	// Create and render the root-level menu. This will in turn
	// create and render it's own child menus.
	var pk = this.$el.attr("data-pk" || null);
	console.log('Rendering MenuView with ID: ' + pk);
	this.rootMenu = new MenuItemCollectionView({id: pk});
	this.$el.html(this.rootMenu.render().el);
    }

});
