define(['underscore', 'backbone', 'menuitems/models'], function (_, Backbone, models) {


    'use strict';


    var MenuItemCollection = Backbone.Collection.extend({

        fetch: function (options) {
            // Ensure we always set the root param when fetching.
            options = options ? _.clone(options) : {};
            options.data = options.data || {};
            options.data.root = this.parentId;
            return MenuItemCollection.__super__.fetch.call(this, options);
        },

        initialize: function (parentId) { // TODO: Should be models, options - this may be a problem
            this.parentId = parentId;
        },

        model: models.MenuItem,

        url: '/admin/menus/menuitem/api/menuitems/'  // TODO

    });


    return {
        'MenuItemCollection': MenuItemCollection
    };

});
