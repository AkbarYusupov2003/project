$( document ).ready(function() {

  const endpoint = "ws://" + window.location.host + window.location.pathname;
  const own_pk = document.getElementById("own_pk").value;
  const buddy_pk = document.getElementById("buddy_pk").value;
  var scroll = $("#messages-body");
  scroll.animate({scrollTop: scroll.prop("scrollHeight")});
  var socket = new WebSocket(endpoint);

  socket.onopen = async function(event){
    $('#send-message-form').on('submit', async function (event){
      event.preventDefault();
      let message = $("#input-message").val();
      let data = JSON.stringify({"message": message});
      socket.send(data);
      $(this)[0].reset();
    })
    document.getElementById("thread_status_submit").addEventListener(
      "click",
      async function(){
        const thread_status = document.getElementById("thread_status").value;
        if (thread_status == "deactivate") {
          socket.close();
          $.ajax({
            url: "",
            type: "POST",
            data: JSON.stringify({ thread_status: thread_status }),
            success: function(json){
              location.reload();
            }
          });
        }
      }
    );
  }

  socket.onmessage = async function(event){
    const data = JSON.parse(event.data);
    const message_pk = data["message_pk"];
    const message = data["message"];
    const created_at = data["created_at"];
    const sender_pk = data["sender_pk"];
    if (own_pk == sender_pk) {
      message_element = `
        <div class="own-message text-dark text-break">
          ${message}<br>
          <small class="mb-0 text-secondary">${created_at}</small>
        </div>
      `;
    } else if (buddy_pk == sender_pk) {
      message_element = `
        <div class="buddy-message text-dark text-break">
          ${message}<br>
          <small class="mb-0 text-secondary">${created_at}</small>
        </div>
      `;
      $.ajax({url: "", type: "POST", data: JSON.stringify({ message_pk: message_pk })});
    } else {
      document.getElementById("from_another_thread").style.display = "block";
    }
    scroll.append(message_element);
    scroll.animate({scrollTop: scroll.prop("scrollHeight")});
  }

  socket.onclose = async function(e){
    document.getElementById("disconnected").style.display = "block";
  }

});
