$(function(){
  // var ws = new WebSocket("ws://192.168.1.224:8765/");
  //var ws = new WebSocket("ws://localhost:8765");

  var gameTime = 60;

  $("#send_num").on("click", function(){
    const num = Number($("#num").val())
    console.log(num);
    //ws.send(JSON.stringify({"type":"manager", "data":num}));

    // 送ったら隠す
    $("#register").hide()
  });

  // スタート画面
  function start_page(){
    console.log("start_page")
    $("#start").show();
    $("#start_game").show()
    $("#count").hide();
    $("#playing").hide();
    $("#result").hide();

    // ボタンを押して開始
    $("#start_game button").on("click", function(){
      $("#count").show();
      $("#start_game").hide()

      $("#count").text(3);
      // カウントダウン
      var count = 0;
      var counter = setInterval(function(){
        count++;
        $("#count").text(3-count);
        if(count > 3){
          clearInterval(counter);
          // 画面切り替え
          playing_page()
        }
      }, 1000);

      // ラズパイに送信
      ws.send(JSON.stringify({"type":"start"}));
    });
  }

  // プレイ中の画面
  function playing_page(){
    console.log("playing_page")
    $("#playing").show();
    $("#start").hide();
    $("#result").hide();

    $("#time").text("Start!!");
    // 残り時間表示
    var count = 0;
    var counter = setInterval(function(){
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
    $("#playing").hide();

    // 30秒で次へ
    var count = 0;
    var counter = setInterval(function(){
      count++;
      $("#time").text(30-count);
      if(count > 30){
        clearInterval(counter);
        // 画面切り替え
        start_page()
      }
    }, 1000);

    // もしくはボタンが押されたら次へ
    $("#go_next").on("click", function(){
      clearInterval(counter);
      // 画面切り替え
      start_page();
    });
  }


  result_page();
})
