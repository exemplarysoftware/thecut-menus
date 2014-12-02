define(['backbone', 'contenttypes/models'], function (Backbone, models) {


    'use strict';


    var ContentObjectCollection = Backbone.Collection.extend({

        model: models.ContentObject

    });


    var ContentTypeCollection = Backbone.Collection.extend({

        model: models.ContentType,

        url: '/admin/menus/menuitem/api/contenttypes/'  // TODO

    });


    return {
        'ContentObjectCollection': ContentObjectCollection,
        'ContentTypeCollection': ContentTypeCollection
    };


});
