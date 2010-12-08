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
  
  $('#menuitem_set-group .form-row.content_type select').live('change', function() {
    var object_select = $(this).closest('fieldset').find('.form-row.object_id select');
    var content_type_pk = $(this).val();
    updateObjectSelect(object_select, content_type_pk);
  });
  
  $('#menuitem_set-group .form-row select').live('change', function() {
    var label = $(this).closest('.inline-related').find('.inline_label');
    updateInlineLabel(label);
  });
  
  $('#menuitem_set-group .form-row.object_id input').each(function() {
    var input = $(this);
    var object_select = $('<select />').attr('id', input.attr('id')).attr('name', input.attr('name'));
    var content_type_pk = input.closest('fieldset').find('.form-row.content_type select').val();
    var input_value = input.val();
    input.replaceWith(object_select);
    updateObjectSelect(object_select, content_type_pk, input_value);
  });
  
  $('#menuitem_set-group .inline-related h3 .inline_label').live('click', function() {
    $(this).hide().closest('.inline-related').find('.form-row.name').show();
    $(this).closest('.inline-related').find('.form-row.name input').select();
  });
  
  $('#menuitem_set-group .form-row.name').live('focusout', function() {
    $(this).hide();
    label = $(this).closest('.inline-related').find('.inline_label');
    updateInlineLabel(label);
    label.show();
  });
  
});

function updateObjectSelect(object_select, content_type_pk, object_select_value) {
  object_select.empty().append('<option value="">---------</option>').val('');
  if (content_type_pk) {
    $.ajax({
      url: $('link[rel="menuitem_contenttype_list"]').attr('href') + content_type_pk + '/',
      success: function(data) {
        $.each(data, function(index, item) {
          var option = $('<option />').attr('value', item.pk).html(item.name);
          object_select.append(option);
        });
        if (object_select_value) {object_select.val(object_select_value);}
      },
    });
  }
}

function updateInlineLabel(label) {
  var input_text = label.closest('.inline-related').find('.form-row.name input').val();
  var object_text = label.closest('.inline-related').find('.form-row.object_id option:selected').text();
  if (input_text) {label.text(input_text);}
  else {label.text(object_text);}
}

