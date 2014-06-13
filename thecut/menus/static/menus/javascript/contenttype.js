var ContentType = Backbone.Model.extend({

    url: function() {
    	return "/admin/menus/menuitem/api/contenttypes/contenttype/" + this.id + "/";
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

    populateContentObjectSelect: function(el, active, active_content_object) {
	// Populate and return the given <select> element with options
	// corresponding to this collection of ContentType models.

	// Force update of the ContentType to get the list of objects.
	var active_content_type = this.findWhere({id: active});
	active_content_type.fetch({async: false});
	//console.log(JSON.stringify(active_content_type, null, 4));

	active_content_type.get('objects').forEach(function(contentObject) {
	    if (contentObject.id == active_content_object) {
		el.append('<option selected="selected" value="' + contentObject.id + '">' + contentObject.name + '</option>');
	    } else {
		el.append('<option value="' + contentObject.id + '">' + contentObject.name + '</option>');
	    }
	});
	return el;
    }

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
