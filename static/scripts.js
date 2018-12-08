$(() => {
  $('.container').on('click', '.like', event => {
    event.preventDefault();
    msg_id = $(event.target)
      .closest('form')
      .attr('data');
    $.post(`/messages/${msg_id}/like`, {}, response => {
      $(event.target).toggleClass('far fas');
    });
  });

  $('.add-message').submit(e => {
    e.preventDefault();
    $('#newMessageModal').modal('toggle'); //or  $('#IDModal').modal('hide');
    return false;
  });
});
