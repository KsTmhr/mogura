$(function(){

  var gameTime = 10;
  var count = 0;
  var rank = 0;

  //var ws = new WebSocket("ws://localhost:8765");
  var ws = new WebSocket("ws://10.0.1.3:8765");


  // サーバーからのメッセージ受信時のイベント
  ws.onmessage = function(message){

    data = JSON.parse(message["data"]);

    if(data["type"] == "info"){
      console.log(data["data"]);
    }
    else if(data["type"] == "rank"){
      rank = data["data"]
      $("#rank").text(rank + 1);

      if(data["data"] < 9){
        $("#info").text("Top10に入りました！！名前を登録して下さい")
        $("#input_name").show();
      }
    }
  }


  $("#send_name").on("click", function(){
    const name = $("#name").val();
    ws.send(JSON.stringify({"type":"name", "data":{"rank":rank, "name":name}}));

    // 送ったら隠す
    $("#input_name").hide();
    $("#info").text("送信しました");
  });

  // ボタンを押して開始
  $("#start_game button").on("click", function(){
    $("#count").text("");
    $("#count").show();
    $("#start_game").hide()

    // カウントダウン
    let count = 0;
    let counter = setInterval(function(){
      count++;
      $("#count").text(4-count);
      if(count > 3){
        // ラズパイに送信
        ws.send(JSON.stringify({"type":"start"}));
        // 画面切り替え
        playing_page()
        clearInterval(counter);
      }
      console.log(counter)
    }, 1000);

  });


// もしくはボタンが押されたら次へ
  $("#go_next").on("click", function(){
    clearInterval(counter);
    // 画面切り替え
    start_page();
  });


  $("#send_num").on("click", function(){
    const num = Number($("#num").val())
    console.log(num);
    ws.send(JSON.stringify({"type":"manager", "data":num}));

    // 送ったら隠す
    $("#register").hide()
  });

  // スタート画面
  function start_page(){
    console.log("start_page");
    $("#start").show();
    $("#start_game").show();
    $("#count").hide();
    $("#playing").hide();
    $("#result").hide();
  }

  // プレイ中の画面
  function playing_page(){
    console.log("playing_page")
    $("#playing").show();
    $("#start").hide();
    $("#result").hide();

    $("#time").text("Start!!");
    // 残り時間表示
    count = 0;
    counter = setInterval(function(){
      count++;
      $("#time").text(gameTime - count);
      if(count > gameTime){
        clearInterval(counter);
        // 画面切り替え
        result_page()
      }
    }, 1000);

  }

  // 結果発表ページ
  function result_page(){
    console.log("result_page")
    $("#result").show();
    $("#start").hide();
    $("#input_name").hide();
    $("#playing").hide();

    $("#rank").text("");
    $("#info").text("")

    // 30秒で次へ
    count = 0;
    counter = setInterval(function(){
      count++;
      $("#go_next").text("開始画面へ戻る　　" + String(30-count));
      if(count > 30){
        clearInterval(counter);
        // 画面切り替え
        start_page()
      }
    }, 1000);
  }


  start_page();
})
