var MenuItem = Backbone.Model.extend({

    initialize: function() {
	console.log('Initializing MenuItem model with ID: ' + this.id);
	this.children = new MenuItemCollection();
	this.children.parentId = this.id;
    },

    url: function() {
	return "/admin/menus/menuitem/api/menuitems/menuitem/" + this.id + "/";
    },

});


var MenuItemCollection = Backbone.Collection.extend({

    model: MenuItem,

    initialize: function(parentId) {
	console.log('Initiliazing MenuItemCollection with parent ID: ' + parentId);
	this.parentId = parentId;
    },

    url: function() {
	// Only the children of this collection's parent should be
	// included.
	var base_url = "/admin/menus/menuitem/api/menuitems/";
	return base_url + "?root=" + this.parentId;
    }

});


var MenuItemView = Backbone.View.extend({

    // HTML & CSS attributes.
    template: _.template($("#menuitem-template").html()),
    tagName: 'li',
    className: 'menuitem',

    attributes: function() {
	return {
	    'data-pk': this.model.get('id'),
	};
    },

    events: {
	'click .edit.button': 'allowEditing',
	'click .save.button': 'save',
	'click .delete.button': 'destroy',
	'change select.contenttype': 'updateContentType',
	'change select.contentobject': 'updateContentObject',
    },



    // Standard view functions.

    render: function() {
	// Render the contents of this single MenuItem.
	console.log('Rendering MenuItem.')
	this.$el.html(this.template(this.model.toJSON()));

	// Insert any children this MenuItem might have.
	if ( this.model.get('is_menu') ) {
	    console.log('Inserting child MenuItems.');
	    ul = $('<ul />', {'data-pk': this.model.get('id')});
	    this.children = new MenuItemCollectionView({'el': ul});
	    this.children.render();
	    this.$el.append(ul);
	}
	return this;
    },

    save: function() {
	// Persist the changes made to the model.
	var nameValue = $(this.el).find("input.name").val().trim();
	this.model.save({name: nameValue});

	// Put the form fields into a non-editable state.
	this.preventEditing();
    },

    destroy: function() {
	this.model.destroy();
    },


    // Custom functions.

    populateContentObjectSelect: function(contentTypes) {
	// Populate and enable the content object selector.
	var el = $(this.el).find("select.contentobject");
	el.empty();
	el.removeClass("disabled").addClass("enabled");
	el.prop("disabled", false);
	var contentType = new ContentType({id: this.model.get('content_type')});
	contentType.fetch({async: false});
	return contentType.getContentObjectSelect(el, this.model.get('object_id'));
    },

    updateContentType: function() {
	var selector = $(this.el).find('select.contenttype');
	this.model.set({content_type: selector.val()});
	var contentTypes = new ContentTypeCollection();
	contentTypes.fetch({async: false});
	this.populateContentObjectSelect(contentTypes);
	this.updateContentObject();
    },

    updateContentObject: function() {
	var select = $(this.el).find('select.contentobject');
	this.model.set({object_id: parseInt(select.val(), 10)});
    },

    allowEditing: function() {
	// Put the form into an editable state.

	// Make the 'name' field editable.
	var nameField = $(this.el).find("input.name");
	nameField.removeClass("disabled").addClass("enabled");
	nameField.prop("disabled", false);

	// Disable the 'Edit' button.
	var editButton = $(this.el).find("input.edit.button");
	editButton.addClass("disabled").removeClass("enabled");
	editButton.prop("disabled", true);

	// Enable the 'Save' button.
	var saveButton = $(this.el).find("input.save.button");
	saveButton.removeClass("disabled").addClass("enabled");
	saveButton.prop("disabled", false);

	// Populate and enable the content type selector.
	var selector = $(this.el).find("select.contenttype");
	selector.empty();
	var contentTypes = new ContentTypeCollection();
	var active = this.model.get('content_type');
	contentTypes.fetch({async: false});
	contentTypes.populateContentTypeSelect(selector, active);
	selector.removeClass("disabled").addClass("enabled");
	selector.prop("disabled", false);
	this.populateContentObjectSelect(contentTypes);
    },

    preventEditing: function() {
	// Make the 'name' field non-editable.
	var nameField = $(this.el).find("input.name");
	nameField.addClass("disabled").removeClass("enabled");
	nameField.prop("disabled", true);

	// Enable the 'Edit' button.
	var editButton = $(this.el).find("input.edit.button");
	editButton.removeClass("disabled").addClass("enabled");
	editButton.prop("disabled", false);

	// Disable the 'Save' button.
	var saveButton = $(this.el).find("input.save.button");
	saveButton.addClass("disabled").removeClass("enabled");
	saveButton.prop("disabled", true);

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


var MenuItemCollectionView = Backbone.View.extend({

    tagName: 'ul',

    initialize: function() {
	var menuItemId = this.$el.attr("data-pk" || null);
	console.log('Initializing MenuItemCollectionView with ID: ' + menuItemId);
	this.collection = new MenuItemCollection(menuItemId);
	this.collection.on('destroy', this.menuItemDestroyed, this);
    },

    render: function() {
	this.$el.empty();
	this.collection.fetch({async: false});

	this.collection.each(function(menuitem) {
	    var itemView = new MenuItemView({model: menuitem});
	    this.$el.append(itemView.render().el);
	}, this);

	return this;
    },

    menuItemDestroyed: function() {
	this.render();
    }

});
