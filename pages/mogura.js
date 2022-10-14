$(function(){
  // var ws = new WebSocket("ws://192.168.1.224:8765/");
  var ws = new WebSocket("ws://localhost:8765");

  // サーバーからのメッセージ受信時のイベント
  ws.onmessage = function(message){

    data = JSON.parse(message["data"]);
    console.log(data);
  }

  $("#send_num").on("click", function(){
    const num = $("#num").val()
    console.log(num);
    ws.send(JSON.stringify({"type":"manager", "data":num}));

    // 送ったら隠す
    $("#num").hide()
    $("#send_num").hide()
  });
})
