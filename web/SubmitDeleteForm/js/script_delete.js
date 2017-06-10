//最終結果を格納する変数
var daySelectVal = -1;
var deleteAppointNum = -1;
var dBandName = "";
var dDay = -1;
var dStart = -1;

//自分が開いていない時，自分を開き，他を閉じる，自分が開いている時，全て閉じる
var tabClasses = ["daySelect", "appointItem"];
function myToggle(mine, time){
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
        myToggle(cName, 150);
    });
});

//最初の処理
$(function() {
  $("dd.daySelectBack").show(); //最初の項目なのであらかじめ表示しておく。
  getDatesData(); //テキストから現在の予約データを読み込む
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
        $("dd.daySelectBack").append(selButton);
    }
});

var startSelectOkFlag = 0;
$(function() {
    $(document).on('click', '.dayButton', function(){
        var date = $(this).text();
        $(".daySelect").text(date);
        var dayVal = $(this).attr("class").split(" ");
        daySelectVal = Number(dayVal[0].replace("day", ""));
        dDay = date;
        setAppointItem();
        myToggle(tabClasses[1], 150); //予約選択へ
    });
});

//////////////↓予約選択↓///////////////
var colorCode = ["#ffffff", "#000000","#808080","#c0c0c0","#ffffff","#ff00ff","#800080","#800000","#ff0000","#ffff00","#00ff00","#008000","#008080", "#0000ff", "#000080", "#00ffff", "#808000"];

function setAppointItem(){
    var items = [];
    for(var i = 0; i < apDates.length; i ++){
            if(apDates[i][1] == daySelectVal){
                items.push([apDates[i][0], apDates[i][2], apDates[i][3], apDates[i][5], apDates[i][2] + apDates[i][3], i]);
            }
    }
    if(items.length >= 2){
        items.sort(
            function(a,b){
                if(a[4] < b[4])return -1;
                if(a[4] > b[4])return 1;
                return 0;
            }
        );
    }
    initAppointItem();
    var bandTag = "";
    var str = "";
    for(var i = 0; i < items.length; i ++){
        bandTag = "<p class=\"colorButton colorButtonExpress col" + items[i][3] + "\">" + items[i][0] + "</p>";
        str =  items[i][1] + "時" + String(items[i][2] * 30) + "分";
        //$("dd.appointItemBack").append("<p class=\"appointItemButton apb" + i + "\">" + str + "</p>");
        $("dd.appointItemBack").append("<p class=\"appointItemButton apb" + i + "\"></p>");
        $(String(".apb" + i)).append("<p class=appointItemButtonExpress>" + str + "</p>");
        $(String(".apb" + i)).append(bandTag);
    }
    var sel;
    for(var i = 0; i < colorCode.length; i ++){
        sel = $(String(".col" + i));
        if(sel){
            sel.css('border-color', colorCode[i]); 
        }
    }
}

function initAppointItem(){
    $("dd.appointItemBack").empty();
    $(".appointItem").empty();
    $(".appointItem").append("削除したい予約");
    deleteAppointNum = -1;
    dBandName = "";
    dStart = -1; 
}

//$("dd.appointItemBack").text("最初に日付を選択してください．")



$(function() {
    $(document).on('click', '.appointItemButton', function(){
       var apVal = $(this).attr("class").split(" ");
        deleteAppointNum = Number(apVal[0].replace("apb", ""));
        nums = $(this).text().match(/^(\d+時\d+分)(\S+)/);
        dBandName = nums[2];
        dStart = nums[1];
        $(".appointItem").empty();
        $(".appointItem").append($(this).html());
        myToggle(tabClasses[1], 150); //すべて閉じる
    });
});

//////////////↓削除確定ボタン↓///////////////
//この関数で削除確定を決定するボタンを使用可能にするか決める.
function changeSubmitDecideButton(){
    if(deleteAppointNum == -1){
        $(".submitButton").addClass("unselSubmitButton");
    }else{
        $(".submitWarning").remove(); //警告文がある場合、削除
        $(".submitButton").removeClass("unselSubmitButton");
    }
}

$(function() {
  changeSubmitDecideButton();
  
  $(document).on('click', '.submitButton', function(){
    if(deleteAppointNum == -1){
        $(".submitWarning").remove();
        $("dl").append("<p class=\"submitWarning\">削除する予約を選択してください.</p>");
        //showModalScreen("予約に成功できなかったっす");
    }else{
        //とりあえずデータを送ってみる
        sendInfoDelete(dBandName, dDay, daySelectVal, dStart, deleteAppointNum);      
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