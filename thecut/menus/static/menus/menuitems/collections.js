define(['backbone', 'menuitems/models'], function(Backbone, models) {


    'use strict';


    var MenuItemCollection = Backbone.Collection.extend({

        model: models.MenuItem,

        initialize: function(parentId) {
            this.parentId = parentId;
        },

        url: function() {
            // Only the children of this collection's parent should be
            // included.
            var base_url = '/admin/menus/menuitem/api/menuitems/';
            return base_url + '?root=' + this.parentId;
        },

    });


    return {
        'MenuItemCollection': MenuItemCollection
    };

});
