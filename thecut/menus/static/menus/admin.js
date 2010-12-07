$(document).ready(function() {
  
  $('a.action.addmenu, a.action.additem').live('click', function(event) {
    var menu = $(this).closest('.menu');
    $.ajax({
      url: $(this).attr('href'),
      success: function(data) {
        $.ajax({
          url: location.href,
          success: function(data) {
            menu.html($(data).find('#' + menu.attr('id')).html());
            bindSortableFancybox();
          },
        });
        },
      error: function() {alert('An error occured whilst processing this request.');},
    });
  event.preventDefault;
  return false;
  });
  
  $('form').live('submit', function(event) {
    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: $(this).serialize(),
      success: function(data) {location.reload();},
      error: function() {alert('An error occured whilst processing this request.');},
    });
  event.preventDefault;
  return false;
  });
  
  $('a.action.delete').live('click', function(event) {
    $.ajax({
      type: 'POST',
      url: $(this).attr('href'),
      success: function(data) {
        $('li#menuitem-' + data.pk).fadeOut().remove();
        $.fancybox.close();
        },
      error: function() {alert('An error occured whilst processing this request.');},
    });
  event.preventDefault; 
  return false;
  });
  
  bindSortableFancybox();
});

function bindSortableFancybox() {
  $('.menus-menu ol.menu').sortable({
    //handle: '.move',
    cursor: 'move',
    opacity: 0.6,
    axis: 'y',
    //containment: 'parent',
    update: function(event, ui) {
      var ids = $(this).sortable('toArray');
      var values = new Array();
      $.each(ids, function(index, item) { 
        var value = parseInt(item.match(/.*-(\d+)/)[1]);
        values.push(value)
      });
      $.ajax({
        type: 'POST',
        url: $('link[rel="menuitem_reorder"]').attr('href'),
        data: {'order': values.join(',')},
        error: function() {alert('An error occured whilst processing this request.');},
      });
    },
  });
  
  $('.menus-menu .menu .source a.action.edit').fancybox({    
    'padding': 20,
    'showCloseButton': false,
    'overlayColor': '#000000',
    'overlayOpacity': '0.8',
    'onComplete': function() {replaceObjectInput();}
  });
}

function replaceObjectInput() {
  /* Replace object input with select */
  var object_input = $('input[name="object_id"][type="text"]');
  if (object_input.length) {
    var object_select = $('<select />').attr('id', object_input.attr('id')).attr('name', object_input.attr('name'));
    var input_value = object_input.val();
    object_input.replaceWith(object_select);
    updateObjectSelect(input_value);
    $('select[name="content_type"]').change(function() {updateObjectSelect();});
  }
}

function updateObjectSelect(input_value) {
  var content_type_pk = $('select[name="content_type"]').val();
  var content_type_list_url = $('link[rel="menuitem_contenttype_list"]').attr('href');
  
  var object_select = $('select[name="object_id"]');
  
  /* Populate object select */
  object_select.empty().append('<option value="">---------</option>').val('');
  if (content_type_pk) {
    $.ajax({
      url: content_type_list_url + content_type_pk + '/',
      success: function(data) {
        $.each(data, function(index, item) {
          var option = $('<option />').attr('value', item.pk).html(item.name);
          object_select.append(option);
        });
        if (input_value) {object_select.val(input_value);}
      },
    });
  }
  
}

