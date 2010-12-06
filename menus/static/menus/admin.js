$(document).ready(function() {
  
  $('.menus-menu ul.menu').sortable({
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
  
  $('.menus-menu .menu .source .action.edit').click(function(event) {
    $('#content-ajax').load($(this).attr('href'));
    event.preventDefault;
    return false;
    });
  
  $('.menus-menu .menu .target .action.edit').click(function(event) {
    alert('Not Implemented');
    event.preventDefault;
    return false;
    });
  
  $('.menus-menu .menu .action.addmenu').click(function(event) {
    $('#content-ajax').load($(this).attr('href'));
    event.preventDefault;
    return false;
    });
  
  $('.menus-menu .menu .action.additem').click(function(event) {
    $('#content-ajax').load($(this).attr('href'));
    event.preventDefault; 
    return false;
    });
  
  $('#content-ajax form').live('submit', function(event) {
    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: $(this).serialize(),
      success: function(data) {location.reload();},//$('#content-ajax').html(data);},
      error: function() {alert('An error occured whilst processing this request.');},
    });
    event.preventDefault;
    return false;
  });
  
  $('#content-ajax a.action.delete').live('click', function(event) {
    $.ajax({
      type: 'POST',
      url: $(this).attr('href'),
      success: function(data) {location.reload();},//$('#content-ajax').html(data);},
      error: function() {alert('An error occured whilst processing this request.');},
    });
    event.preventDefault; 
    return false;
    });
  
});
