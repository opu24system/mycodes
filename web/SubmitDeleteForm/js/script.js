//最終結果を格納する変数
var bandNameVal = "";
var frameColorVal = 0;
var daySelectVal = -1;
var startSelectVal = -1;
var hourSelectVal = -1;

//自分が開いていない時，自分を開き，他を閉じる，自分が開いている時，全て閉じる
var tabClasses = ["bandName", "frameColor", "daySelect", "startSelect"];
function myToggle(mine, time){
    upDateBandName(); //バンド名が入っていれば更新
    changeSubmitDecideButton(); //予約確定ボタンを更新
    for(var i = 0; i < tabClasses.length; i ++){
        var sel = $('.' + tabClasses[i]);
        if(tabClasses[i] === mine){
            sel.next().slideToggle(time);
        }else{
            sel.next().slideUp(time);
        }
    }
}

//アコーディオンメニューのタブをクリックした時の挙動
$(function() {
    $(document).on('click', '.tigger dt', function(){
        var cName = $(this).attr('class');
                   
        if(cName === "startSelect"){
            changeStartDecideButton(); //開始時刻タブのみ別処理
        }
        myToggle(cName, 150);
    });
});

//////////////↓バンド名↓///////////////
function upDateBandName(){
    name = $(".bandNameForm").val();
    if(name !== ""){
        //$(".bandName").text(name);
        bandNameVal = name;

        //おまかせの場合，乱数取得
        if(frameColorVal == 0){
            frameColorVal = 1 + Math.floor(Math.random() * (colorStr.length - 1));
        }
        $(".bandname").html("<p class=\"colorButton colorButtonExpress col" + frameColorVal + "\">" + name + "</p>");
        $(String(".col" + frameColorVal)).css('border-color', colorCode[frameColorVal]); 
        
    }else{
        $(".bandName").text("バンド名");
        bandNameVal = "";
    }
}

var nameInput = "<input class=bandNameForm type=\"text\" name=\"txtb\" value=\"\">";
var decideButton = "  <p class=bandNameDecideButton>OK</p>";
function decideBandName(){
    upDateBandName()
    
    if(daySelectVal != -1){
        myToggle(tabClasses[0], 150); //次の項目が入力済みならば全て閉じる
    }else{
        myToggle(tabClasses[2], 150); //次の項目を自動で開く
    }
}

$(function() {
  $("dd.bandNameBack").append(nameInput);
  $("dd.bandNameBack").append(decideButton);
  appendFrameColorBack();
  
  $("dd.bandNameBack").show(); //最初の項目なのであらかじめ表示しておく。
  
  
  getDatesData(); //テキストから現在の予約データを読み込む
  
  $(".bandNameDecideButton").addClass("gButton");
  
  //ここではとりあえず初期値として日付が選択されていない場合を初期値とし、先に日付を選んでもらう感じにする
  $("dd.startSelectBack").html("<p class=startSelectInit>日付を選択してください</p>");
});
$(function() {
  $(document).on('click', '.bandNameDecideButton', function(){
        decideBandName();
    });
  
  $(".bandNameForm").keypress(function(e){
        if( e.which == 13 ){
          decideBandName();
          return false;
        }
    });
});


//////////////↓枠の色↓///////////////
var colorStr = ["おまかせ", "黒","グレー","シルバー","白","ピンク","紫","栗色","赤","黄","ライム","緑","青緑", "青", "ネイビー", "アクア", "オリーブ"];
var colorCode = ["#ffffff", "#000000","#808080","#c0c0c0","#ffffff","#ff00ff","#800080","#800000","#ff0000","#ffff00","#00ff00","#008000","#008080", "#0000ff", "#000080", "#00ffff", "#808000"];
//class = colorButton col1, ...
//class = colorButton col2, ...
//みたいにしてみました
function colorButtons(colorNum){
    return "<p class=\"colorButton col" + colorNum + "\">" + colorStr[colorNum] + "</p>";
}

function appendFrameColorBack(){
    var parentSel = $("dd.bandNameBack");
    
    for(var i = 0; i < colorStr.length; i ++){
        parentSel.append(colorButtons(i));
        var sel = String(".col" + i);
        $(sel).css('border-color', colorCode[i]);        
    }
    
    $(".col0").css("background", "#ffda55");
    
    for(var i = 0; i < 1;  i++){
        parentSel.append("<p class=\"colorButton colorButtonFake\">ああ</p>");
    }
}

$(function() {
    $(document).on('click', '.colorButton', function(){
        //var color = $(this).text();
        //$(".frameColor").text("枠の色 : " + color);
        
        var colorVal = $(this).attr("class").split(" ");
        colorVal[1] = Number(colorVal[1].replace("col", ""));
        
        //おまかせの場合，乱数取得
        if(colorVal[1] == 0 || colorVal[1] == -1){
            frameColorVal = 1 + Math.floor(Math.random() * (colorStr.length - 1));
        }
        else{
            frameColorVal = colorVal[1];
        }
        
        //背景色を初期化
        var sel;
        for(var i = 0; i < colorStr.length; i ++){
            sel = String(".col" + i);
            $(sel).css('background', "");        
        }
        $(this).css("background", "#ffda55");
    });
});

//////////////↓日付↓///////////////
var dayList = ["日", "月", "火", "水", "木" ,"金" ,"土"];

$(function() {
    //曜日に応じて処理し、必ず金曜始まりになり，来週の月曜日を予約する場合、次の金曜日を待つことになる。
  
    //var nowDay= new Date();
    var nowDay = new Date();
    var today = nowDay.getDay();

    if(today - 5 < 0){
        today += 2;
    }else{
        today -= 5;
    }
    fridayNum = nowDay.getTime() - (86400000 * today);

    for(var i = 0; i < 10; i ++){
        var dayObj = new Date(fridayNum + 86400000 * i);
        var buttonStr = zeloFill(dayObj.getMonth() + 1) + "/" + zeloFill(dayObj.getDate()) + "(" + dayList[dayObj.getDay()]  + ")";
        var selButton =   "<p class=\"day" + i + " dayButton\">" + buttonStr + "</p>";
        var unselButton = "<p class=\"day" + i + " dayButton unselDayButton\">" + buttonStr + "</p>";
  
        if(i < today){
            $("dd.daySelectBack").append(unselButton);
        }else{
            $("dd.daySelectBack").append(selButton);
        }
    }
});

var startSelectOkFlag = 0;
$(function() {
    $(document).on('click', '.dayButton', function(){
        var date = $(this).text();
        $(".daySelect").text(date);
        var dayVal = $(this).attr("class").split(" ");
        daySelectVal = Number(dayVal[0].replace("day", ""));
        
        initStartSelectButton();
        startUnselDecide();
        unselStartTime();
                   
        if(startSelectOkFlag == 0){
            startSelectOk();
            startSelectOkFlag = 1;
        }
    
        myToggle(tabClasses[3], 150); //日付を更新すると、次の開始時間の項目は必ず更新されるので、自動で開くようにする
    });
});

//////////////↓開始時刻↓///////////////
var ajaxFlag = 0; //通信中の場合1になる?
var apDates = []; //予約済みの時間などを放り込んでおく配列
var unselTime = []; //予約不能な時間がpushされている
var halfUnsel; //~時30分など、選択不能にならないが、30分の選択では半分だけ予約不能になるものを入れておく

//以下の変数に値が入っているかどうかで全ての開始時刻にまつわるボタンが押されたか判断する
var startTime = -1;
var thirtyTime = -1;
var praLength = -1;
var amPm = -1;

//日付が選択された時、予約不能位置を格納しておく
function startUnselDecide(){
    unselTime = [];
    for(var i = 0; i < apDates.length; i ++){
        //選択した日のうち、24 * 2 = 48マスのうち予約不能な部分を決定
        if(apDates[i][1] == daySelectVal){
            for(j = 0; j < apDates[i][4]; j ++){
                unselTime.push(apDates[i][2] * 2 + apDates[i][3] + j);
            }
        }
    }
    unselTime.sort(function(a,b){
        if( a < b ) return -1;
        if( a > b ) return 1;
        return 0;
    });
    initStartUnselButton();
}

//予約済みの時間を選択不能にする。最初に初期化として全ての選択不能を解除する
function unselStartTime(){
    initStartUnselButton();
    var flag = -1;
    halfUnsel = unselTime.slice(0); //~時30分など、ここでは選択不能にならないが、30分の選択で処理が必要なものを入れておく
    
    for(var i = 0; i < unselTime.length; i ++){
        if(unselTime[i] % 2 == 0){
            flag = unselTime[i];
        }else{
            if(unselTime[i] == flag + 1){
                var className = String("sTime" + Math.floor(unselTime[i] / 2));
                var sel = $('.' + className);
                sel.addClass("unselStartTimeButton");
                halfUnsel[i] = -1;
                halfUnsel[i-1] = -1;
                flag = -1;
            }else{
                flag = -1;
            }
        }
    }
}

//押された開始時間ボタンに合わせ、~時0分30分ボタンを更新。引数timeは0-24の整数を入れる
function upDateThirtyButton(time){
    $(".startThirtyButton").removeClass("unselStartTimeButton");
    for(var i = 0; i < halfUnsel.length; i ++){
        if(i == -1 || time != Math.floor(halfUnsel[i] / 2))continue;
        //halfUnsel内の-1でない要素について、偶数なら0分を、奇数なら30分を選択不能する
        if(halfUnsel[i] % 2 == 0){
            $(".thir0").addClass("unselStartTimeButton");
            if(Number(thirtyTime) / 30 == 0){
                $(".thir0").css('border-color', "");
                thirtyTime = -1;
    
                $(".startLengthButton").css('border-color', "");
                $(".startLengthButton").addClass("unselStartTimeButton"); //初期状態は選択不能
            }
        }else{
            $(".thir1").addClass("unselStartTimeButton");
            if(Number(thirtyTime) / 30 == 1){
                $(".thir1").css('border-color', "");
                thirtyTime = -1;
                
                $(".startLengthButton").css('border-color', "");
                $(".startLengthButton").addClass("unselStartTimeButton"); //初期状態は選択不能
            }
        }
        break;
    }
}

//押された開始時間ボタン、30分ボタンに合わせ、時間の長さボタンを更新.timeは0-24, thirtyは0,30
function upDateTimeLengthButton(time, thirty){
    var big = -1;
    var nowTime = time * 2 + thirty/30;
    var unselNum = 0;
    
    
    $(".startLengthButton").css('border-color', "");
    $(".startLengthButton").addClass("unselStartTimeButton"); //長さボタン初期化
    praLength = -1;
    
    $(".startLengthButton").removeClass("unselStartTimeButton");
    for(var i = 0; i < unselTime.length; i ++){
        if(unselTime[i] > nowTime){
            big = unselTime[i];
            break;
        }
    }
    if(big == -1){
        big = 48;
    }
    
    if(big - nowTime >= 5){
        unselNum = 0;
    }else{
        unselNum = 4 - (big - nowTime);
    }
    
    for(var i = 0; i < unselNum; i ++){
        var str = '.len' + String(3 - i);
        $(str).addClass("unselStartTimeButton");
    }
}

//開始時刻などにまつわる選択不能を初期化する
function initStartUnselButton(){
    $(".startSelectButton").removeClass("unselStartTimeButton"); //初期化
    $(".startThirtyButton").removeClass("unselStartTimeButton");
    $(".startLengthButton").addClass("unselStartTimeButton"); //初期状態は選択不能
}

//開始時刻などにまつわるものを初期化
function initStartSelectButton(){
    startTime = -1;
    thirtyTime = -1;
    praLength = -1;
    amPm = -1;
    startSelectVal = -1;
    hourSelectVal = -1;
    $(".stbPm").hide();
    $(".stbAm").hide();
    //とりあえずボーダースタイルしかいじってないので、ここだけ初期化
    //他をいじるならそこも初期化が必要
    $("dd.startSelectBack").children().css('border-color', "");
    $(".startTimeBack").children().css('border-color', "");
    $(".startSelect").text("練習時間");
}

//日付が選択された時、この関数を使い内容を変更する(最初のクリック時のみ)
function startSelectOk(){
    selBack = $("dd.startSelectBack");

    $(".startSelectInit").remove();
    selBack.append("<p class=\"startExpress se1\">開始時刻</p><BR>");
    
    selBack.append("<p class=\"startAmPmButton startAm\">午前</p>　　");
    selBack.append("<p class=\"startAmPmButton startPm\">午後</p><BR>");
    
    //午前午後でクラスを分ける
    selBack.append("<p class=\"startTimeBack stbAm\"></p>");
    selBack.append("<p class=\"startTimeBack stbPm\"></p>");
    
    var amBack = $(".stbAm");
    var pmBack = $(".stbPm");
    var stBack = $(".startTimeBack");
    var nowBack = amBack;
    for(var i = 0; i < 24; i ++){
        if(i % 6 == 0 && i != 0 && i != 12){
            nowBack.append("<BR>");
        }
        if(i <= 11){
            nowBack = amBack;
            nowBack.append("<p class=\"startSelectButton sTime" + i + " \">" + i + "</p> ");
        }else{
            nowBack = pmBack;
            nowBack.append("<p class=\"startSelectButton sTime" + i + " \">" + String(i - 12) + "</p> ");
        }
    }
    stBack.append("<BR>");
    stBack.append("<p class=\"startThirtyButton thir0\">" + 0 + "分</p> ");
    stBack.append("<p class=\"startThirtyButton thir1\">" + 30 + "分</p><BR>");
    
    stBack.append("<p class=\"startExpress se2\">練習時間</p><BR>");
    stBack.append("<p class=\"startLengthButton len0\">30分</p> ");
    stBack.append("<p class=\"startLengthButton len1\">1時間</p><BR> ");
    stBack.append("<p class=\"startLengthButton len2\">1時間30分</p> ");
    stBack.append("<p class=\"startLengthButton len3\">2時間</p><BR>");
    $(".startLengthButton").addClass("unselStartTimeButton");
    
    stBack.append("<p class=startOkButton>OK</p><BR>");
    changeStartDecideButton(); //最初は開始時刻タブを使用不可に
}

//この関数で開始時刻を決定するボタンを使用可能にするか決める.
function changeStartDecideButton(){
    if(startTime == -1 || thirtyTime == -1 || praLength == -1){
        $(".startOkButton").addClass("unselStartOkButton");
    }else{
        $(".startExpressWarning").remove(); //警告文がある場合、削除
        $(".startOkButton").removeClass("unselStartOkButton");
    }
}

$(function() {
  $(document).on('click', '.startAmPmButton', function(){
    var cName = $(this).attr('class');
    unselStartTime();

    if(cName === "startAmPmButton startAm"){
        $(".startPm").css('border-color', "#DDD");
        $(this).css('border-color', "#f00");
        $(".stbAm").show(150);
        $(".stbPm").hide(150);
        amPm = 0;
    }else{
        $(".startAm").css('border-color', "#DDD");
        $(this).css('border-color', "#f00");
        $(".stbPm").show(150);
        $(".stbAm").hide(150);
        amPm = 1;
    }
    
    if(startTime >= 12 && amPm == 0)startTime -= 12;
    if(startTime <= 11 && amPm == 1)startTime += 12;
    startText = startTime + "時";
    
    
    $(".startThirtyButton").css('border-color', "");
    $(".startThirtyButton").addClass("unselStartTimeButton"); //30分ボタン初期化
    $(".startLengthButton").css('border-color', "");
    $(".startLengthButton").addClass("unselStartTimeButton"); //長さボタン初期化
    praLength = -1;

    changeStartDecideButton();
  });
  
  $(document).on('click', '.startSelectButton', function(){
    startTime = Number($(this).text()) + (amPm * 12);
    $(".startSelectButton").css('border-color', ""); //全ての開始時間ボタンを初期化
    var startSelectVal = -1;
    $(this).css('border-color', "#f00");
    startText = startTime + "時";
    upDateThirtyButton(startTime);
                 
    if(Number(thirtyTime) != -1){
        upDateTimeLengthButton(startTime, Number(thirtyTime));
    }
    changeStartDecideButton();
  });
  
  $(document).on('click', '.startThirtyButton', function(){
    thirtyTime = $(this).text().replace("分", "");;
    $(".startThirtyButton").css('border-color', "");
    $(this).css('border-color', "#f00");
        
    upDateTimeLengthButton(startTime, Number(thirtyTime));
    changeStartDecideButton();
  });
  
  
  $(document).on('click', '.startLengthButton', function(){
    praLength = $(this).text();
    $(".startLengthButton").css('border-color', "");
    $(this).css('border-color', "#f00");
    hourSelectVal = Number($(this).attr("class").split(" ")[1].replace("len", "")) + 1;
    changeStartDecideButton();
  });
  
  $(document).on('click', '.startOkButton', function(){
    if(startTime == -1 || thirtyTime == -1 || praLength == -1){
        /*$(".startExpressWarning").remove();
        $("dd.startSelectBack").append("<p class=\"startExpress startExpressWarning\">開始時刻と練習時間を指定してください.</p>");*/
    }else{
        startSelectVal = Number(startTime) * 2 + Number(thirtyTime) / 30;
        //hourSelectVal += Number(praLength);クリックしたときに行う
        $(".startSelect").text(startTime + "時" + thirtyTime + "分から" + praLength);
        changeSubmitDecideButton();
        $(".startSelect").next().slideToggle(150);  //最後の項目なのでmyToggle関数は使わない
    }
  });
});

//////////////↓予約確定ボタン↓///////////////
//この関数で予約確定を決定するボタンを使用可能にするか決める.
function changeSubmitDecideButton(){
    if(bandNameVal === "" || frameColorVal == -1 || daySelectVal == -1 || startSelectVal == -1 || hourSelectVal == -1){
        $(".submitButton").addClass("unselSubmitButton");
    }else{
        $(".submitWarning").remove(); //警告文がある場合、削除
        $(".submitButton").removeClass("unselSubmitButton");
    }
}

//予約がかぶってないかチェック.繁忙期なら普通にあり得るので必ず必要
function checkInfo(day, start, thirty, hour){
    getDatesData(); //apDatesを更新して最新の情報に
    //while(ajaxFlag == 1){}; //通信終了まで待つ
    for(i = 0; i < apDates.length; i ++){
        if(day == apDates[i][1]){
            var spointtex = apDates[i][2] * 2 + apDates[i][3];
            var epointtex = spointtex  + apDates[i][4] - 1;
            
            var spointin = start * 2 + thirty;
            var epointin = spointin + hour - 1;

            if( (spointtex <= spointin && spointin  <= epointtex) ||
               (spointtex <= epointin && epointin  <= epointtex) ||
               ((spointin <= spointtex && spointtex  <= epointin) &&
                (spointin <= epointtex && epointtex  <= epointin))
               ){
                return -1;
            }
        }
    }
    return 0;
}

$(function() {
  changeSubmitDecideButton();
  
  $(document).on('click', '.submitButton', function(){
    if(bandNameVal === "" || frameColorVal == -1 || daySelectVal == -1 || startSelectVal == -1 || hourSelectVal == -1){
        $(".submitWarning").remove();
        $("dl").append("<p class=\"submitWarning\">全ての項目を決定してください.</p>");
        //showModalScreen("予約に成功できなかったっす");
    }else{
        var startHour = 0;
        var thirtyMinutes = 0;
        if(startSelectVal % 2 == 0){
            startHour = startSelectVal / 2;
            thirtyMinutes = 0;
        }else{
            startHour = Math.floor(startSelectVal / 2);
            thirtyMinutes = 1;
        }
                 
        if(checkInfo(daySelectVal, startHour, thirtyMinutes, hourSelectVal) == -1){
            showModalScreen("<BR>既に予約されています。<BR><BR>時間を変更してください。<BR><BR>", false);
        }else{
            //予約成功の場合
            sendInfo(bandNameVal, daySelectVal, startHour, thirtyMinutes, hourSelectVal, frameColorVal);      
        }
         initStartSelectButton();
         //initStartUnselButton();
         startUnselDecide();
         unselStartTime();
         changeSubmitDecideButton();
         getDatesData();
    }
  });
});

//////////////↓モーダルスクリーン↓///////////////
var closeButton = "<BR><p class=\"modalExpress modalExButton modalClose\">閉じる</p>";
var appointMoveButton = "<BR><p class=\"modalExpress modalExButton modalAppoint\">予約表へ</p>";
function showModalScreen(html, showAppointButton){
    centeringModalSyncer();
    $(".modalExpressParent").html(html);
    if(showAppointButton){
        $(".modalExpressParent").append(appointMoveButton);
    }
    $(".modalExpressParent").append(closeButton);
    //[$modal-overlay]をフェードインさせる
    $(".modalBack , .modalExpress").fadeIn(300);
}
//センタリングをする関数
function centeringModalSyncer(){
	var w = $(window).width();
	var h = $(window).height();
	var mcSel = $(".modalExpress");
	var cw = mcSel.outerWidth(true);
	var ch = mcSel.outerHeight(true);
	var pxleft = ((w - cw)/2);
	var pxtop = ((h - ch)/2);
	mcSel.css({"left": pxleft + "px"});
	mcSel.css({"top": pxtop + "px"});
}
$(window).resize(centeringModalSyncer);

//モーダル閉じるボタン
$(function() {
    $(document).on('click', '.modalBack , .modalClose', function(){
		$( ".modalBack, .modalExpress" ).fadeOut(300);
    });
});

//予約表へボタン
$(function() {
    $(document).on('click', '.modalAppoint', function(){
        //window.location.href = passAppointCGI;
        // http://exapmple.com/xxx/123 → http://example.com/xxx/aiueo
        history.replaceState('','','konappoint/appoint.cgi');
        window.location.href = window.location.href ;
    });
});