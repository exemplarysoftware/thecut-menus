define(['backbone', 'contenttypes/models'], function (Backbone, models) {

    'use strict';


    var ContentObjectCollection = Backbone.Collection.extend({

        model: models.ContentObject,

    });


    var ContentTypeCollection = Backbone.Collection.extend({

        model: models.ContentType,
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


    return {
        'ContentObjectCollection': ContentObjectCollection,
        'ContentTypeCollection': ContentTypeCollection
    };

});
