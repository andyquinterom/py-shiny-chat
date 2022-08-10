function bind_chatbox(id) {
    $(document).keydown(function(event){
      var keycode = (event.keyCode ? event.keyCode : event.which);
      if(keycode == '13') {
          $("#" + id + "-enviar").click();
      }
    });
}
