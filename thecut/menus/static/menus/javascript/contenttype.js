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


var ContentTypeCollectionView = Backbone.View.extend({

    tagName: 'select',
    className: 'contenttype',

    initialize: function(contentTypeId) {
	this.selected = contentTypeId;
	this.collection = new ContentTypeCollection();
    },

    render: function() {
	this.$el.empty();
	this.collection.fetch({async: false});

	this.collection.each(function(contentType) {
	    if ( this.selected == contentType.get('id')) {
		this.$el.append('<option selected="selected" value="' +
				contentType.get('id') + '">' +
				contentType.get('verbose_name') +
				'</option>');
	    } else {
		this.$el.append('<option value="' +
				contentType.get('id') + '">' +
				contentType.get('verbose_name') +
				'</option>');
	    }
	}, this);

	return this;
    }

});

var ContentObjectSelectView = Backbone.View.extend({

    tagName: 'select',
    events: {
	'click': 'refreshContentObjects'
    },

    refreshContentObjects: function() {
	console.log('Refresh the <select> of content objects.')
    }

});


var ContentObject = Backbone.Model.extend({

    defaults: {
	'id': null,
	'name': '',
    }

});


var ContentObjectCollection = Backbone.Collection.extend({

    model: ContentObject,

});


var ContentObjectView = Backbone.View.extend({

    tagName: 'select',
    className: 'contentobject',

    render: function() {
	console.log('Rendering content object view');
	console.log(JSON.stringify(this.collection));
	this.$el.empty();

	this.collection.each(function(contentObject) {
	    // TODO: replace with template?
	    this.$el.append('<option value="' +
			    contentObject.get('id') + '">' +
			    contentObject.get('name') +
			    '</option>');
	}, this);

	return this;
    }

});
