$(function(){
  //var ws = new WebSocket("ws://192.168.1.224:8765/");
  //var ws = new WebSocket("ws://localhost:8765");
  var ws = new WebSocket("ws://10.0.1.3:8765");

  var score = [];
  var name = [];
  var tbody = $('tr');

  for(let i=0; i<10; i++){
  	score[i] = tbody.children("td.score").eq(i);
  }

  for(let i=0; i<10; i++){
    name[i] = tbody.children("td.name").eq(i);
  }

  // サーバーからのメッセージ受信時のイベント
  ws.onmessage = function(message){

    data = JSON.parse(message["data"]);
    console.log(data);
    if(data["type"] == "top"){
      for(let i=0; i<10; i++){
        score[i].text(data["data"]["rank"][i]);
        name[i].text(data["data"]["name"][i]);
      }
    }
  }

  setTimeout(function(){
    // サーバーへメッセージ送信
    ws.send(JSON.stringify({"type":"ranking"}));
    ws.send(JSON.stringify({"type":"get_top"}));
  }, 3000)
})
