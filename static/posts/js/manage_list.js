function accept(obj)
{
  const activity_pk = obj.getAttribute("data-pk");
  $.ajax({
    url: 'accept/',
    type: 'POST',
    data: JSON.stringify({ activity_pk: activity_pk }),
    success: function(json){
      document.getElementById(activity_pk).remove();
    }
  });
}

function reject(obj)
{
  const activity_pk = obj.getAttribute("data-pk");
  const comment = obj.getAttribute("data-comment");
  $.ajax({
    url: 'reject/',
    type: 'POST',
    data: JSON.stringify({ activity_pk: activity_pk, comment: comment }),
    success: function(json){
      document.getElementById(activity_pk).remove();
    }
  });
}