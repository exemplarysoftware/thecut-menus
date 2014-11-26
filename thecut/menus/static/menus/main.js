var menusRequire = requirejs.config({

    baseUrl: document.querySelector('script[data-app="menus"][src$="/main.js"]').getAttribute('data-baseUrl'),

    context: 'menus',

    paths: {
        'backbone': 'lib/backbone',
        'domReady': 'lib/domReady',
        'jquery': 'lib/jquery',
        'jquery-ui': 'lib/jquery-ui',
        'underscore': 'lib/underscore'
    },

    shim: {
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
        }
    }

});


menusRequire(

    ['jquery', 'menuitems/views', 'domReady!'],

    function ($, menuitemsViews) {

        'use strict';

        // Set up AJAX requests to include Django's CSRF token.
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        // Set us up the page.
        var rootMenu = new menuitemsViews.MenuView();
        rootMenu.render();

    }
);
