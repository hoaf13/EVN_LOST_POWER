$(document).ready(function(){
    $('#nickname').focus();
    $('#reload-btn').prop("disabled",true);
    $('#send-btn').prop('disabled',true)
    $('#nickname').keypress(function(e){
      if(e.keyCode==13 && $('#send-btn').prop("disabled") == true)  
      $('#send-btn-nickname').click(); 
    });

    $('#my-message').keypress(function(e){
      if(e.keyCode==13 && $('#send-btn').prop("disabled") == false)
      $('#send-btn').click();
    });
    
    var socket = io();
    $('#send-btn-nickname').on('click', ()=>{
      if ($('#nickname').val().trim() === ''){
        alert("Khong duoc de trang")
      }
      else{
        socket.emit('client-start-chat', $('#nickname').val())
        $('#reload-btn').prop("disabled",false);
        $('#send-btn-nickname').prop("disabled",true);
        $('#nickname').prop("disabled",true);
        $('#send-btn').prop("disabled",false);
        $('#my-message').prop('disabled',false);
        $('#my-message').focus()
      }
    });
    socket.on('server-start-chat', (msg)=>{
      $('.box').append('<li class="bot-msg">' + msg + '<li>')
    });
    
    $('#send-btn').on('click', ()=>{
      var input_msg = $('#my-message').val()
      if (input_msg.trim() === ''){
        alert("Khong duoc de trang")
      }
      else{
        $('.box').append('<li class="client-msg">' + input_msg + '<li>')
        $('#my-message').val('')
        var ans = {}
        ans['message'] = input_msg
        ans['sender'] = $('#nickname').val()
        socket.emit('client-send-msg', ans)
      }
    });
    socket.on('server-send-msg', (msg) => {
      console.log("server-send-msg: " + msg)
      $('.box').append('<li class="bot-msg">' + msg + '<li>')
    });

    $('#reload-btn').on('click',function() {
        $(this).prop("disabled",true);
        $("#send-btn-nickname").prop("disabled", false)
        $('#send-btn').prop("disabled",true);
        $('#nickname').prop("disabled",false);
        $("#nickname").val('')
        $('#my-message').val('')
        $('.box').empty()
        $('#nickname').focus()
    });
    
    socket.on('server-send-action-all-field',()=>{
      console.log("action_all_field")
      socket.emit("client-send-action-all-field", $('#nickname').val());  
    });

    socket.on('server-send-action-provide-address', ()=>{
      console.log("action_provide_address")
      socket.emit('client-send-action-provide-address', $('#nickname').val());
    });
    
    socket.on('server-end',()=>{
      $('#my-message').prop('disabled',true);
      $('#send-btn').prop("disabled",true);    
    });

  });