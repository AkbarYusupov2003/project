function filter_visibility()
{
  if($("#visibility").is(":checked")){
    $("#filter").show();
  } else {
    $("#filter").hide();
  }
}
function load_more(obj)
{
  const pk = obj.getAttribute("data-pk");
  document.getElementById(`load-${pk}`).style.display = "";
  obj.remove();
}
function reply(obj)
{
  const pk = obj.getAttribute("data-pk");
  document.getElementById("reply_pk").value = pk;
}
function send_reply()
{
  const reply_pk = document.getElementById("reply_pk").value;
  const reply_comment = document.getElementById("reply_comment").value;
  $.ajax({
    url: 'activity-reply/',
    type: 'POST',
    data: JSON.stringify({ reply_pk: reply_pk, reply_comment: reply_comment }),
    success: function(json){
      document.getElementById(`activity-${reply_pk}`).remove();
      document.getElementById("reply_comment").value = "";
    }
  });
}
function report(obj)
{
  const pk = obj.getAttribute("data-pk");
  document.getElementById("report_pk").value = pk;
}
function send_report()
{
  const report_reason = document.getElementById("report_reason").value;
  if (report_reason) {
    const report_message = document.getElementById("report_message").value;
    const report_pk = document.getElementById("report_pk").value;
    $.ajax({
      url: 'activity-report/',
      type: 'POST',
      data: JSON.stringify({ report_pk: report_pk, report_message: report_message, report_reason: report_reason }),
      success: function(json){
        document.getElementById(`activity-${report_pk}`).remove();
        document.getElementById("report_message").value = "";
      }
    });
  }
}