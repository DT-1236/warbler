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
});
