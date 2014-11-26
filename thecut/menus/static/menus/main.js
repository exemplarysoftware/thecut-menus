var menusRequire = requirejs.config({

    baseUrl: document.querySelector('script[data-app="menus"][src$="/main.js"]').getAttribute('data-baseUrl'),

    context: 'menus',

    paths: {
        'backbone': 'lib/backbone',
        'backbone.babysitter': 'lib/backbone.babysitter',
        'backbone.marionette': 'lib/backbone.marionette',
        'backbone.wreqr': 'lib/backbone.wreqr',
        'domReady': 'lib/domReady',
        'jquery': 'lib/jquery',
        'jquery-ui': 'lib/jquery-ui',
        'json2': 'lib/json2',
        'underscore': 'lib/underscore'
    },

    shim: {
        'backbone': {
            deps: ['json2', 'jquery', 'underscore'],
            exports: 'Backbone'
        },
        'backbone.babysitter': {
            deps: ['json2', 'backbone'],
            exports: 'Backbone.ChildViewContainer'
        },
        'backbone.marionette': {
            deps: ['json2', 'jquery', 'underscore', 'backbone',
                   'backbone.wreqr', 'backbone.babysitter'],
            exports: 'Backbone.Marionette'
        },
        'backbone.wreqr': {
            deps: ['json2', 'backbone'],
            exports: 'Backbone.Wreqr'
        },
        'jquery': {
            exports: 'jQuery',
            init: function () {
                'use strict';
                return this.jQuery.noConflict(true);
            }
        },
        'jquery-ui': {
            deps: ['jquery'],
            exports: 'jQueryUi'
        },
        'json2': {
            exports: 'JSON'
        },
        'underscore': {
            exports: '_'
        }
    }

});


menusRequire(

    ['jquery', 'csrf', 'backbone.marionette', 'menuitems/views', 'domReady!'],

    function ($, csrf, Marionette, menuitemsViews) {


        'use strict';


        var $root = $('#menu'),
            application = new Marionette.Application();


        // Define application regions
        application.addRegions({
            'root': $root
        });


        // Add menu application initializer
        application.addInitializer(function () {
            var rootMenuView = new menuitemsViews.MenuItemCollectionView({
                id: this.getRegion('root').$el.attr('data-pk')
            });
            this.getRegion('root').show(rootMenuView);
        });


        // Start application
        application.start();


    }

);
