function _builds_filter_selected(o, d) {
  data = $(d.element).data('.moksha_selectable_data');
  if (data.show_secondary_tables) {
    $('.secondary_table').fadeIn();
  } else {
    $('.secondary_table').fadeOut();
  }

  var main_table = $('.main_table');
  $('h3', main_table).html(data.label);
  $('table', main_table).mokshagrid("request_update", {filters: data.filters});
}