
var apDates = []; //予約済みの時間などを放り込んでおく配列

//テキストから予約済みの時間を取得
function getDatesData()
{
    $.ajax({
        type: 'GET',
        url: "konappoint/appointdata/data.txt",
        async: false,
        cache: false,
        dataType: 'text',
        success: function(data) {
            var infos = data.split("\n");
            apDates[i] = [];
            for(var i = 0; i < infos.length; i ++){
                apDates[i] = infos[i].split(",");
                if(apDates[i].length <= 1){
                    continue;
                }
                
                for(var j = 0; j < apDates[i].length; j ++){
                    if(j != 0){
                        apDates[i][j] = Number(apDates[i][j]);
                    }
                }
            }
        },error:function() {
 　　　alert('ファイルの読み込みに失敗しました');
        }
    });
}

//phpに情報を送る
function sendInfo(sName, sDay, sStart, sThirty, sHour, sFcolor){
    var daySelectText = $(".daySelect").text();
    var startSelectText = $(".startSelect").text();
    var sHistry = getHistryString(bandNameVal,  daySelectText, startSelectText, "appoint");
    $.ajax({
        type: 'POST',
        url: 'sendData.php',
        //async: false,
        context: $('.tigger dt').index(this) + 1,
        data : {
           name   : sName,
           day    : sDay,
           start  : sStart,
           thirty : sThirty,
           hour   : sHour,
           fcolor : sFcolor,
           histry : sHistry,
        }
    }).done(function(data, status, xhr) {
        //初期化
        if(data == "OK"){
            initSecondTime();
            var info = "<p class=modalAppointInfo>" + bandNameVal + "<BR>" + 
                            daySelectText + "<BR>" +
                            startSelectText + "</p>";
            showModalScreen("予約に成功しました<BR>" + info, true);
        }else{
            alert("既に予約されています.時間を変更してください");
        }
    }).fail(function(xhr, status, error) {
            alert("通信エラーが発生しました.もう一度試してみてください.");
    }).always(function(arg1, status, arg2) {
        // 通信完了時の処理
    });
}

//phpに情報を送る(削除バージョン)
function sendInfoDelete(dName, dDay, dDayNum, dStart, deleteAppointNum){
    var sHistry = getHistryString(dName, dDay, dStart,"delete");
    startTime = dStart.match(/^(\d+)時(\d+)分/);
    $.ajax({
        type: 'POST',
        url: 'sendDataDelete.php',
        //async: false,
        context: $('.tigger dt').index(this) + 1,
        data : {
           //deleteNum   : deleteAppointNum,
           day : dDayNum,
           startHour : startTime[1],
           startMin : String(Number(startTime[2]) / 30),
           histry : sHistry,
        }
    }).done(function(data, status, xhr) {
        if(data == "OK"){
            var info = dDay + "<BR>" + $(".appointItem").html();
            setAppointItem();
            showModalScreen("削除に成功しました<BR><BR>" + info + "<BR>", true);
        }else{
             alert("削除できませんでした．既に削除されている可能性があります.");
        }
    }).fail(function(xhr, status, error) {
        alert("通信エラーが発生しました.もう一度試してみてください.");
        //予約表へ飛ぶ
    }).always(function(arg1, status, arg2) {
        // 通信完了時の処理
    });
}

function getHistryString(apName, apDay, apStart, type){
    var hiduke=new Date();
    var month = zeloFill(hiduke.getMonth()+1);
    var day = zeloFill(hiduke.getDate());
    var hour = zeloFill(hiduke.getHours());
    var minute = zeloFill(hiduke.getMinutes());
    var second = zeloFill(hiduke.getSeconds());
    if(type == "appoint"){
        return month + "/" + day + "," + hour + ":" + minute + ":" + second + ",予約," +  apDay + apStart + " " + "\'" + apName + "\'" + "\n" ;
    }else{   
        return month + "/" + day + "," + hour + ":" + minute + ":" + second + ",削除," +  apDay + apStart + "から始まる " + "\'" + apName + "\'" + "\n" ;
    }
}

function zeloFill( number ) {
	return ( "0" + number ).substr( -2 ) ;
}
