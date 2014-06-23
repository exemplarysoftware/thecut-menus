$(document).ready(function() {

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
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
	}
    });

    // Set us up the page.
    var itemsview = new MenuItemCollectionView({'el': $('#menuitems')});
    itemsview.render();

    // Make menu items sortable.
    $('#menuitems, #menuitems ul').sortable({
	'cursor': 'move',
	'handle': '.move.button',
        'update': function(event, ui) {
            $.ajax({
                'data': $(this).closest('ul').sortable('serialize', {'key': 'pk', 'attribute': 'data-sortable-pk'}),
                'error': function(XMLHttpRequest, textStatus, errorThrown) {
                  alert('An error occured whilst processing this request.');
                },
                'type': 'POST',
                'url': '/admin/menus/menuitem/api/menuitems/menuitem/' + $(this).closest('ul').attr('data-pk') + '/reorder/',
            });
	}
    });

});
