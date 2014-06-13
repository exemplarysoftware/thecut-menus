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
	'click .edit.button': 'edit',
	'click .save.button': 'save',
	'change select.contenttype': 'update_contenttype',
	'change select.contentobject': 'update_contentobject',
    },

    render: function() {
	var ul = $("#menuitems");
	var li = $(this.el).html(this.template(this.model.toJSON()));
	ul.append(li);
	return this;
    },

    update_contenttype: function() {
	var selector = $(this.el).find('select.contenttype');
	console.log('Update content type to: ' + selector.val());
	this.model.set({content_type: selector.val()});
    },

    update_contentobject: function() {
	var selector = $(this.el).find('select.contentobject');
	console.log('Current value of object_id: ' + JSON.stringify(this.model.get('object_id')));
	console.log('Update content object to: ' + selector.val());
	var new_object_id = {
	    "id": parseInt(selector.val(), 10),
//	    "name": $(selector).find('option:selected').text()
	};
	this.model.set({object_id: parseInt(selector.val(), 10)});
//	this.model.get('object_id').name = 
	console.log('New value of object_id:' + JSON.stringify(this.model.get('object_id')));
    },

    edit: function() {
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
	var active = this.model.get('content_type').id;
	contentTypes.fetch({async: false});
	contentTypes.populateContentTypeSelect(selector, active);
	selector.removeClass("disabled").addClass("enabled");
	selector.prop("disabled", false);

	// Populate and enable the content object selector.
	var selector = $(this.el).find("select.contentobject");
	selector.empty();
	var active_content_object = this.model.get('object_id');
	contentTypes.populateContentObjectSelect(selector, active, active_content_object);
	selector.removeClass("disabled").addClass("enabled");
	selector.prop("disabled", false);

    },

    save: function() {
	// Put the form into a non-editable state.

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

	// Persist the changes made to the model.
	var name_value = $(this.el).find("input.name").val().trim();

	console.log('Saving model: ' + JSON.stringify(this.model));
	this.model.save({name: name_value});
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
