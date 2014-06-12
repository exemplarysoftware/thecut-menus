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
	'click .save.button': 'save'
    },

    render: function() {
	var ul = $("#menuitems");
	var li = $(this.el).html(this.template(this.model.toJSON()));
	ul.append(li);
	return this;
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


$(document).ready(function() {

    // Set up AJAX requests to include Django's CSRF token.
    function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
		var cookie = jQuery.trim(cookies[i]);
		// Does this cookie string begin with the name we want?
		if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
		}
            }
	}
	return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
	crossDomain: false, // obviates need for sameOrigin test
	beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
	}
    });

    // Set us up the page.
    var itemsview = new MenuItemsView();
    itemsview.render();

});
