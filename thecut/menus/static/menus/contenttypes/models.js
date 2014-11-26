define(['backbone'], function (Backbone) {

    'use strict';

    var ContentType = Backbone.Model.extend({

        url: function () {
            return '/admin/menus/menuitem/api/contenttypes/contenttype/' + this.id + '/';
        },

        getContentObjectSelect: function (el, activeId) {
            // Return the given <select> element with options corresponding to
            // this ContentType's possible choices of object_id.
            this.get('objects').forEach(function (contentObject) {
                if (activeId !== null && contentObject.id === activeId) {
                    el.append('<option selected="selected" value="' + contentObject.id + '">' + contentObject.name + '</option>');
                } else {
                    el.append('<option value="' + contentObject.id + '">' + contentObject.name + '</option>');
                }
            });
            return el;
        }

    });


    var ContentObject = Backbone.Model.extend({

        defaults: {
            'id': null,
            'name': ''
        }

    });


    return {
        'ContentObject': ContentObject,
        'ContentType': ContentType
    };

});
