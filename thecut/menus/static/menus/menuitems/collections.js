define(['underscore', 'backbone', 'menuitems/models'], function (_, Backbone, models) {


    'use strict';


    var MenuItemCollection = Backbone.Collection.extend({

        fetch: function (options) {
            // Ensure we always set the root param when fetching.
            options = options ? _.clone(options) : {};
            options.data = options.data || {};
            options.data.root = this.parentModel.get('id');
            return MenuItemCollection.__super__.fetch.call(this, options);
        },

        initialize: function (models, options) {
            options = options ? _.clone(options) : {};
            this.parentModel = options.parentModel;
        },

        model: models.MenuItem,

        url: '/admin/menus/menuitem/api/menuitems/'  // TODO

    });


    return {
        'MenuItemCollection': MenuItemCollection
    };

});
