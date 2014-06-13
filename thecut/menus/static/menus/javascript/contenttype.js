var ContentType = Backbone.Model.extend({

    url: function() {
    	return "/admin/menus/menuitem/api/contenttypes/contenttype/" + this.id + "/";
    },

    getContentObjectSelect: function(el, activeId) {
	// Return the given <select> element with options
	// corresponding to this ContentType's possible choices of
	// object_id.
	this.get('objects').forEach(function(contentObject) {
	    if (activeId != null && contentObject.id == activeId) {
		el.append('<option selected="selected" value="' + contentObject.id + '">' + contentObject.name + '</option>');
	    } else {
		el.append('<option value="' + contentObject.id + '">' + contentObject.name + '</option>');
	    }
	});
	return el;
    }


})


var ContentTypeCollection = Backbone.Collection.extend({

    model: ContentType,
    url: "/admin/menus/menuitem/api/contenttypes/",

    populateContentTypeSelect: function(el, active) {
	// Populate and return the given <select> element with options
	// corresponding to this collection of ContentType models.
	this.forEach(function(contentType) {
	    if (contentType.get('id') == active) {
		el.append('<option selected="selected" value="' + contentType.get('id') + '">' + contentType.get('verbose_name') + '</option>');
	    } else {
		el.append('<option value="' + contentType.get('id') + '">' + contentType.get('verbose_name') + '</option>');
	    }
	});
	return el;
    },


});


var ContentTypeView = Backbone.View.extend({

    tagName: 'select',
    events: {
	'click': 'refreshContentObjects'
    },

    refreshContentObjects: function() {
	console.log('Refresh the <select> of content objects.')
    }
})
