$(document).ready(function() {
  $('#menuitem_set-group').addClass('js-enabled');
  
  $('#menuitem_set-group').sortable({
    //cursor: 'move',
    update: function(event, ui) {
      $('#menuitem_set-group .form-row.order input').each(function(index) {
        $(this).val(index);
      });
    },
  });
});
