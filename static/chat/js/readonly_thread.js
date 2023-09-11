$( document ).ready(function() {
  var scroll = $("#messages-body");
  scroll.animate({scrollTop: scroll.prop("scrollHeight")});
});
