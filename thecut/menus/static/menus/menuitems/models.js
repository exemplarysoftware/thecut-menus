define(['backbone', 'menuitems/constants'], function (Backbone, constants) {


    'use strict';


    var MenuItem = Backbone.Model.extend({

        // For reference, these fields are used when POST/PUTting data up to the
        // server.
        defaults: {
            'id': null,  // The auto-generated ID.
            'title': '',  // Optional title.
            'parent': null,  // Optional ID of parent MenuItem.
            'content_type': null,  // Optional ID of ContentType.
            'content_type_name': null,  // Optional name of ContentType.
            'object_id': null,  // Optional ID of Content Object.
            'content_object': null,  // Display name of content object.
            'is_menu': false,  // Whether the menu item is a sub-menu.
            'state': constants.states.DISPLAY  // Current state of this menu item.
        },

        url: function () {  // TODO
            var url = '/admin/menus/menuitem/api/menuitems/menuitem/';

            if (this.get('id') === null) {
                return url;
            }

            return url + this.get('id') + '/';
        },

        // Toggle between the 'edit' and 'display' states.
        toggleState: function () {
            if (this.get('state') === constants.states.DISPLAY) {
                this.set({state: constants.states.EDIT});
            } else {
                this.set({state: constants.states.DISPLAY});
            }
        }

    });


    return {
        'MenuItem': MenuItem
    };

});
