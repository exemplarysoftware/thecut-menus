define(['backbone'], function (Backbone) {


    'use strict';


    var ContentType = Backbone.Model.extend({

        url: function () {  // TODO
            return '/admin/menus/menuitem/api/contenttypes/' + this.id + '/';
        }

    });


    var ContentObject = Backbone.Model.extend();


    return {
        'ContentObject': ContentObject,
        'ContentType': ContentType
    };


});
