<?php
//include 'ChromePhp.php'; 
//ChromePhp::log($flag);
/* 配列の作成*/
$array = array($_POST['name'], $_POST['day'], $_POST['start'], $_POST['thirty'], $_POST['hour'], $_POST['fcolor']);
/*履歴データの取り出し*/
$histryData = $_POST['histry'];

/* 予約表のデータを更新 */
//$file = fopen("konappoint/appointdata/data.txt", "a");
/* CSVファイルを配列へ */
//if( $file ){
//  var_dump( fputcsv($file, $array) );
//}
/* ファイルポインタをクローズ */
//fclose($file);
$path = "konappoint/appointdata/data.txt";
$fileArray = @file($path);
$flag = false;
  // 取得したファイルデータ(配列)を全て表示する
  for( $i = 0; $i < count($fileArray); ++$i ) {
    list($bName, $bDay, $bStart, $bThirty, $bLength, $bfColor) = split(',' , $fileArray[$i]);
    if($bDay == $array[1] && $bStart == $array[2] && $bThirty == $array[3]){
    	$flag = true;
    }
  }
 
if($flag){
	$flag = "MISS";
}else{
	$flag = "OK";
	array_push($fileArray, implode(",", $array)."\n");
	file_put_contents($path,implode("", $fileArray), LOCK_EX);
	/*履歴のデータを更新*/
	$path = 'konappoint/appointdata/histry.txt';
	$content = $histryData.file_get_contents($path);
	file_put_contents($path,$content, LOCK_EX);
}

header('Content-type: application/json');
echo json_encode($flag);
 
?>