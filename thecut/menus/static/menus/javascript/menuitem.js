var MenuItem = Backbone.Model.extend({

    url: function() {
	return "/admin/menus/menuitem/api/menuitems/menuitem/" + this.id + "/";
    }

});


var MenuItemCollection = Backbone.Collection.extend({

    model: MenuItem,

    url: function() {
	// Only list the MenuItems which are descendants of the
	// MenuItem which is being edited.
	var base_url = "/admin/menus/menuitem/api/menuitems/";
	model_id = $("#menuitems").attr("data-root-menuitem-id" || null);
	if (model_id != null) {
	    return base_url + "?root=" + model_id;
	};

	return base_url;
    }

});


var MenuItemView = Backbone.View.extend({

    tagName: 'li',
    template: _.template($("#menuitem-template").html()),
    events: {
	'click .edit.button': 'allowEditing',
	'click .save.button': 'save',
	'change select.contenttype': 'updateContentType',
	'change select.contentobject': 'updateContentObject',
    },

    render: function() {
	var ul = $("#menuitems");
	var li = $(this.el).html(this.template(this.model.toJSON()));
	ul.append(li);
	return this;
    },

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

    save: function() {
	// Persist the changes made to the model.
	var name_value = $(this.el).find("input.name").val().trim();
	this.model.save({name: name_value});

	// Put the form fields into a non-editable state.
	this.preventEditing();
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
