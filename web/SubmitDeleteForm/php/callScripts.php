<?php
    
    /*
function echoStr($str){
    echo "document.write(\"$str\")";
}
*/

function getEchoStr($str){
    return "document.write(\"$str\")";
}

date_default_timezone_set('UTC');

// スクリプトの更新日付を返す
function echo_filedate($filename) {
  if (file_exists($filename)) {
    $d = date("YmdHis", filemtime($filename));
    //echo "document.write(\"$d\")";
    return $d;
   } else {
    return "file not found";
    //echo "document.write(\"file not found\")";
  }
}

//スクリプトを呼ぶ際に，ファイルの更新日時に合わせてキャッシュの日付を更新する
function call_scripts_date_css($fileName){
    $day = echo_filedate($fileName);
    $s = "<link rel='stylesheet' type='text/css' href='$fileName?date=$day'>";
    //echo "document.write(\"$s\")";
    return getEchoStr($s);
}

function call_scripts_date_js($fileName){
    $day = echo_filedate($fileName);
    $s = "<script type='text/javascript' src='$fileName?date=$day'></script>";
    //echo "document.write(\"$s\")";
    return getEchoStr($s);
}

//css js を呼ぶ，ここにファイルを追加していく
$e = 
call_scripts_date_css('css/style.css') . "\n" .
call_scripts_date_js('js/ajaxFunc.js') . "\n" .
call_scripts_date_js('js/script_appoint.js') . "\n";

echo "$e";

 ?>