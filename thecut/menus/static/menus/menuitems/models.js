define(['backbone'], function(Backbone) {


    'use strict';


    var MenuItem = Backbone.Model.extend({

        initialize: function() {
            this.states = {
                DISPLAY: 'displaying',
                EDIT: 'editing',
            }
            this.set({state: this.states.DISPLAY});
        },

        // For reference, these fields are used when POST/PUTting data up to the
        // server.
        defaults: {
            'id': null,              // The auto-generated ID.
            'title': '',             // Optional title.
            'parent': null,          // Optional ID of parent MenuItem.
            'content_type': '',      // Optional ID of ContentType.
            'content_type_name': '', // Optional name of ContentType.
            'object_id': '',         // Optional ID of Content Object.
            'content_object': '',    // Display name of content object.
            'is_menu': false,        // Whether the menu item is a sub-menu.
            'state': null,           // Current state of this menu item.
        },

        url: function() {
            var url = '/admin/menus/menuitem/api/menuitems/menuitem/'

            if ( this.get('id') == null ) {
                return url;
            }

            return url + this.get('id') + '/';
        },

        // Toggle between the 'edit' and 'display' states.
        toggleState: function() {
            if ( this.get('state') == this.states.DISPLAY ) {
                this.set({state: this.states.EDIT});
            } else {
                this.set({state: this.states.DISPLAY});
            }
        },

    });


    return {
        'MenuItem': MenuItem
    };

});
