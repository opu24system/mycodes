<?php
 
 //ログを見たいときは以下を使用
//include 'ChromePhp.php';
//ChromePhp::log($bName);

//削除データ
// $deleteData = $_POST['deleteNum'];
$day =  $_POST['day'];
$startHour =  $_POST['startHour'];
$startMin = $_POST['startMin'];
 
//履歴データ
$histryData = $_POST['histry'];


$path = "konappoint/appointdata/data.txt";
$fileArray = @file($path);
$flag = false;
  // 取得したファイルデータ(配列)を全て表示する
  for( $i = 0; $i < count($fileArray); ++$i ) {
    list($bName, $bDay, $bStart, $bThirty, $bLength, $bfColor) = split(',' , $fileArray[$i]);
    if($bDay == $day && $bStart == $startHour && $bThirty == $startMin){
    	$fileArray[$i] = "";
    	$flag = true;
    }
  }

if($flag){
    $flag = "OK";
	file_put_contents($path,implode("", $fileArray), LOCK_EX);
	
    //履歴のデータを更新
    $path = 'konappoint/appointdata/histry.txt';
    $content = $histryData.file_get_contents($path);
    file_put_contents($path,$content, LOCK_EX);
}else{
    $flag = "MISS";
}

header('Content-type: application/json');
echo json_encode($flag);

?>