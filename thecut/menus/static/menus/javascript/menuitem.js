var MenuItem = Backbone.Model.extend({

    initialize: function() {
	this.states = {
	    DISPLAY: 'displaying',
	    EDIT: 'editing',
	}
	this.set({state: this.states.DISPLAY});
    },

    // For reference, these fields are used when POST/PUTting data up to the
    // server.
    defaults: {
	'id': null,            // The auto-generated ID.
	'name': '',            // Optional name.
	'parent': null,        // Optional ID of parent MenuItem.
	'content_type': '',    // Optional ID of ContentType.
	'object_id': '',       // Optional ID of Content Object.
	'content_object': '',  // Display name of content object.
	'is_menu': false,      // Whether the menu item is a sub-menu.
	'state': null,         // Current state of this menu item.
    },

    url: function() {
	var url = '/admin/menus/menuitem/api/menuitems/menuitem/'

	if ( this.get('id') == null ) {
	    return url;
	}

	return url + this.get('id') + '/';
    },

    // Toggle between the 'edit' and 'display' states.
    toggleState: function() {
	if ( this.get('state') == this.states.DISPLAY ) {
	    this.set({state: this.states.EDIT});
	} else {
	    this.set({state: this.states.DISPLAY});
	}
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
	'click .edit-save.button': 'editSaveClicked',
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

    destroy: function(event) {
	this.model.destroy();
	event.stopPropagation();
    },


    // Custom functions.

    isEditable: function() {
	var saveButton = $(this.el).children('.form').find(".save.button");
	return saveButton.hasClass("enabled");
    },

    editSaveClicked: function(event) {
	if ( this.model.get('state') == this.model.states.EDIT ) {
	    this.save();
	    this.preventEditing(); // TODO: listen to model change.
	} else {
	    this.allowEditing();   // TODO: listen to model change.
	}
	this.model.toggleState();
	event.stopPropagation();
    },

    populateContentObjectSelect: function(contentTypes) {
	// Populate and enable the content object selector.
	var el = $(this.el).children('.form').find("select.contentobject");

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

    updateContentType: function(event) {
	// Update this item's content type and populate the content
	// object selector with items of the selected type.
	var el = $(this.el).children('.form').find('select.contenttype');

	// The <select> for choosing the content type, won't exist if
	// this is a sub-menu.
	if ( el !== null ) {
	    this.model.set({content_type: el.val()});
	    var contentTypes = new ContentTypeCollection();
	    contentTypes.fetch({async: false});
	    this.populateContentObjectSelect(contentTypes);
	    this.updateContentObject();
	}
	event.stopPropagation();
    },

    updateContentObject: function(event) {
	var select = $(this.el).children('.form').find('select.contentobject');
	if ( select != null) {
	    this.model.set({object_id: parseInt(select.val(), 10)});
	}
	event.stopPropagation();
    },

    allowEditing: function() {
	// Put the form into an editable state.

	// Make the 'name' field editable.
	var nameField = $(this.el).children('.form').find("input.name");
	nameField.removeClass("disabled").addClass("enabled");
	nameField.prop("disabled", false);

	// Disable the 'Edit' button.
	var editButton = $(this.el).children('.form').find(".edit.button");
	editButton.addClass("disabled").removeClass("enabled");

	// Enable the 'Save' button.
	var saveButton = $(this.el).children('.form').find(".save.button");
	saveButton.removeClass("disabled").addClass("enabled");

	// Populate and enable the content type selector.
	var selector = $(this.el).children('.form').find("select.contenttype");
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
	var nameField = $(this.el).children('.form').find("input.name");
	nameField.addClass("disabled").removeClass("enabled");
	nameField.prop("disabled", true);

	// Enable the 'Edit' button.
	var editButton = $(this.el).children('.form').find(".edit.button");
	editButton.removeClass("disabled").addClass("enabled");

	// Disable the 'Save' button.
	var saveButton = $(this.el).children('.form').find(".save.button");
	saveButton.addClass("disabled").removeClass("enabled");

	// Disable the content type select.
	var contentTypeSelect = $(this.el).children('.form').find("select.contenttype");
	contentTypeSelect.addClass("disabled").removeClass("enabled");
	contentTypeSelect.prop("disabled", true);

	// Disable the content object select.
	var contentObjectSelect = $(this.el).children('.form').find("select.contentobject");
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
    },

});


var MenuItemCollectionView = Backbone.View.extend({

    tagName: 'div',
    template: _.template($("#menu-template").html()),
    className: 'menu',
    events: {
	'click .add.menuitem.button': 'addMenuItemButtonClicked',
	'click .add.submenu.button': 'addSubMenuButtonClicked',
	'change .add.menuitem select.contenttype': 'contentTypeChanged',
    },

    initialize: function() {
	this.collection = new MenuItemCollection(this.id);
	this.listenTo(this.collection, 'destroy', this.menuItemDestroyed);
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

	// Render a <select> element for the Content Types.
	var select = this.$el.find('li.menuitem.add select.contenttype');
	var contentTypeSelect = new ContentTypeCollectionView({
	    el: select, contentTypeId: null});
	contentTypeSelect.render();

	// Render a <select> element for the Content Type's Content Objects.
	var selectedContentType = new ContentType({id: select.val()});
	this.renderContentObjectSelect(selectedContentType);

	return this;
    },

    // TODO: handle the add button by calling this.collection.create( formData );
    addSubMenuButtonClicked: function(event) {
	var name = $(this.el).children('ul.controls').children('li.add.submenu').find('input.name').val();
	console.log(name);
	this.collection.create({'name': name,
				'parent': this.collection.parentId});
	// Prevent the event from propagating and firing multiple times. For
	// some reason event.stopPropagation() does not work
	// here. JavaScript. See https://stackoverflow.com/questions/10522562/
	this.render();
	event.stopPropagation();
	return false;
    },

    // TODO: handle the add button by calling this.collection.create( formData );
    addMenuItemButtonClicked: function(event) {
	var name = this.$el.find('li.add.menuitem input.name').val();
	var contentType = this.$el.find('li.add.menuitem select.contenttype').val();
	var contentObject = this.$el.find('li.add.menuitem select.contentobject').val();
	this.collection.create({'name': name, 'content_type': contentType,
				'object_id': contentObject,
				'parent': this.collection.parentId});
	// Prevent the event from propagating and firing multiple times. For
	// some reason event.stopPropagation() does not work
	// here. JavaScript. See https://stackoverflow.com/questions/10522562/
	this.render();
	event.stopPropagation();
	return false;
    },

    contentTypeChanged: function() {
	// TODO: why is this getting called twice? seems to be getting
	// called for both "forms" on the page, but with the data from
	// only the "form" which was actually changed.
	var selected = this.$el.find('li.add.menuitem select.contenttype').val();
	var contentType = new ContentType({id: selected});
	this.renderContentObjectSelect(contentType);
    },

    // Render a <select> element which allows selection of a Content Object for
    // the given Content Type.
    renderContentObjectSelect: function(contentType) {
	contentType.fetch({async: false});
	var objects = contentType.get('objects');
	var contentObjectCollection = new ContentObjectCollection(objects);
	var contentObjectSelect = this.$el.find('li.add.menuitem select.contentobject');
	var contentObjectView = new ContentObjectView({
	    collection: contentObjectCollection,
	    el: contentObjectSelect,
	});
	contentObjectView.render();
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
	this.rootMenu = new MenuItemCollectionView({id: pk});
	this.$el.html(this.rootMenu.render().el);
    }

});
