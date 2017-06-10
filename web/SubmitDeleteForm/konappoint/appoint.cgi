#!/usr/bin/perl

require 'jcode.pl';

#現在の秒数を出す
$genzai = time;

#一週間の秒数を変数へ入れる
#一日は 60*60*24 で 86400秒
#一週間は 86400*7 で604800秒

#曜日は 0～6 の値が返されるので配列で扱う
@wdays = ('日','月','火','水','木','金','土');

$start = $genzai;
($sec,$min,$hour,$mday,$mon,$year,$wno) = localtime($start);
$startday = sprintf("%02d",$mday);
$starthour = $hour;

#必ず金曜始まりにする
if($wno > 5){
    $start -= 86400;
}
elsif($wno < 5){
    $start -= ($wno + 2) * 86400;
}

@sche = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
@schedate = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
@scheday = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
$i = 0;
foreach $tmp (@sche){
    ($sec,$min,$hour,$mday,$mon,$year,$wno) = localtime($start);
    
    $schedate[$i] = sprintf("%02d/%02d", $mon+1,$mday);   
    $scheday[$i] =  sprintf("(%s)", $wdays[$wno]); 
    $tmp = $schedate[$i] . $scheday[$i];
    $i ++;
    $start += 86400;
}

#今日のデータも一応だしとく
($sec,$min,$hour,$mday,$mon,$year,$wno) = localtime($genzai);     
$now = sprintf("%02d/%02d(%s)",$mon+1,$mday,$wdays[$wno]);

#送信されたデータを受け取る
$in = ();
$in{'name'} = 'INITIALIZED';

if ($ENV{'REQUEST_METHOD'} eq 'POST') {
  read(STDIN, $alldata, $ENV{'CONTENT_LENGTH'});
} else {
  $alldata = $ENV{'QUERY_STRING'};
}
foreach $data (split(/&/, $alldata)) {
  ($key, $value) = split(/=/, $data);
  
  $value =~ s/\+/ /g;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1))/eg;
  $value =~ s/\t//g;
  $in{"$key"} = $value;
}

#htmlエスケープ
$in{"name"} =~ s/<.*?>//g;
$in{"dename"} =~ s/<.*?>//g;

#プルダウンの日付を今日にしつつ，昔の日付を選べないようにする．
@day_selcted = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
$dc = 5;
$a = 0;
$dflag = 0;
foreach $tmp (@day_selcted){
    if($startday eq substr($sche[$a],3, 2)){
        $tmp = sprintf("<option value=\"%d\" selected>", $a);
	$dflag = 1;
    }else{        
        if($dflag == 0){
            $tmp = sprintf("<option value=\"%d\" disabled>", $a);
	}
        else{
	    $tmp = sprintf("<option value=\"%d\">", $a);
	}
    }
    $dc ++;
    $a ++;
    if($dc >= 7){
        $dc = 0;
    }
}

print "Content-type: text/html; charset=UTF-8\n\n";
#print "Content-type: text/html; charset=Shift-JIS\n";

#文字化け対策のおまじない
print "<!-- \xfd\xfe(MOJIBAKE TAISAKU)-->\n";
print "<!-- 龠(MOJIBAKE TAISAKU) -->\n";
$mheight = 60;
$mwidth = 40;

$border_msize = '4px';
$border_ssize = '2px';

$btopwidth = $border_msize;
$bbottomwidth = $border_ssize;
$bleftwidth = $border_ssize;
$brightwidth = $border_ssize;
$rightb = 'none';


#表の大きさは24 * 20 = 480マス．１マス30分となる
#とりあえずすべてのマスを初期化
@appdata;

for($a = 0;$a < 20; $a ++){
    for($b = 0; $b < 24; $b ++){

        if($b % 2 == 0){
	    $leftb = 'solid';
        }else{
	    $leftb = 'dotted';
        }
  		
  		if($b == 0){$bleftwidth = $border_msize;}
  		else{$bleftwidth = $border_ssize;}
  		
  		if($b == 23){
  			$brightwidth = $border_msize;
  			$rightb = 'solid'
  		}
  		else {
  			$brightwidth = $border_ssize;
  			$rightb = 'none';
  		}
  		
        if($a % 2 == 0){
            $topb = 'solid';
            $bottomb = 'dashed';
        }else{
            $topb = 'none';
	    	if($a != 19){                
                $bottomb = 'none';         
	    	}else{
                $bottomb = 'solid';
				$bbottomwidth = $border_msize;
	    	}
        }
        $appdata[$a * 24 + $b] = "<td height=$mheight width=$mwidth align=center 
                                      style=\"border-width: $btopwidth $brightwidth $bbottomwidth $bleftwidth;
                                              border-style: $topb $rightb $bottomb $leftb;
                                              word-break: break-all;\"> <!-- ※1 -->
                                      <font size = 1 color=\"#FFFFFF\"></td>\n";
        #word-break: break-all;#border-top-width:$btopwidth; border-bottom-width:$bbottomwidth; 
        #※1 ← word-break: break-all;\">はsub add_appointで使用するので，絶対に変更しない。する場合はadd_appointも変えること。
    }
}

$info = '';
$err = 0;

($sec,$min,$hour,$mday,$mon,$year,$wno) = localtime($start);    
$nowfiletime = $start - $sec - (($min + $hour * 60) * 60) - 86400;
$oldfiletime = $nowfiletime - 604800; 


#ファイルを読み込み、配列に入れる。
open (IN, "appointdata/data.txt");
@text = <IN>;
close (IN);

open (IN, "appointdata/latest.txt");
@latest = <IN>;
close (IN);

if($latest[0] != $nowfiletime){
   $latest[0] = $nowfiletime;
	#表の更新日が記述されたファイルを現在の時間に合わせる
	open (OUT,"+< appointdata/latest.txt");
	flock(OUT, 2);
	truncate(OUT, 0);
	seek(OUT, 0, 0);
	print OUT @latest;
    close (OUT);
    
    @newtext = ();
    
	foreach $tmp (@text){
            my @olddata = split(',', $tmp);
	    #金土日のデータの場合
	    if($olddata[1] >= 7 && $olddata[1] <= 9){	
			$olddata[1] -= 7;
            unshift (@newtext,"$olddata[0],$olddata[1],$olddata[2],$olddata[3],$olddata[4],$olddata[5]\n");
        }
	}
	
	#先週の金土日のデータが追記された配列を，現在のテキストに書き出す
    open (OUT,"+< appointdata/data.txt");
	flock(OUT, 2);
	truncate(OUT, 0);
	seek(OUT, 0, 0);
	print OUT @newtext;
    close (OUT);
    
    @text = @newtext;
}

if($in{'name'} eq 'INITIALIZED'){    
    $info = '';
    $err = 1;
}


#予約確定ボタンが押されたとき
if($in{'appoint'} ne '' && $in{'delete'} eq ''){
    #フォームから受け取った予約がほかのバンドと被ってないかチェック
    foreach $tmp (@text){
        my @intext = split(',', $tmp);

		if($in{'day'} == $intext[1]){
        	my($spointtex) = $intext[2] * 2 + $intext[3];
        	my($epointtex) = $spointtex  + $intext[4] - 1;
	
        	my($spointin) = $in{'hour'} * 2 + $in{'thirty'};
        	my($epointin) = $spointin + $in{'minutes'} - 1;

            #if($in{'name'} eq 'test'){
            #    print "<font size = 7>spin:$spointin, epin:$epointin, spex:$spointtex, epex$epointtex</font>";
            #}
            if( ($spointtex <= $spointin && $spointin  <= $epointtex) ||
    	        ($spointtex <= $epointin && $epointin  <= $epointtex) ||
    	        (($spointin <= $spointtex && $spointtex  <= $epointin) &&
    	         ($spointin <= $epointtex && $epointtex  <= $epointin))
    	      ){
	           $info = 'その時間はすでに予約済みです。';
               $err = 1;
	           last;
           }
        }
    }

    #23時から2時間とか，日をまたぐ予約を禁止する
    if($in{'hour'} * 60 + $in{'thirty'} * 30 + $in{'minutes'} * 30 > 1440){
        $info = '日をまたいでの予約はできません';
        $err = 1;
    }
    #バンド名の入力チェック
    if($in{'name'} eq ''){
        $info = 'バンド名を入力してください';
        $err = 1;
    }

    #エラーがなかった場合，表とテキストファイルを更新する．
    if($err != 1){

        #色がお任せだった場合，お任せの色をランダムに決めておく
        if($in{'fcolor'} == 0){
            $in{'fcolor'} = int(rand 15) + 1;
        }
    
        #表を更新
        &add_appoint($in{'name'}, $in{'day'}, $in{'hour'}, $in{'thirty'}, $in{'minutes'}, $in{'fcolor'}, \@appdata);

        #フォームから受け取ったデータをカンマで区切りつつ配列の先頭に追加する
        unshift (@text,"$in{'name'},$in{'day'},$in{'hour'},$in{'thirty'},$in{'minutes'},$in{'fcolor'}\n");
    
        #新しいデータが追記された配列を test.txt に書き出す
        open (OUT,"+< appointdata/data.txt");
	    flock(OUT, 2);
	    truncate(OUT, 0);
	    seek(OUT, 0, 0);
        print OUT @text;
        close (OUT);
        
        my($alength) = &num_to_applength($in{'minutes'});
        $info = sprintf("%s%d時%d分から%s， '%s' で予約しました。", $sche[$in{'day'}], $in{'hour'}, 30 * $in{'thirty'}, $alength, $in{'name'});
        my($hist) =  sprintf("%s%d時%d分から%s， '%s'", $sche[$in{'day'}], $in{'hour'}, 30 * $in{'thirty'}, $alength, $in{'name'});
        &update_histry($hist, "予約");
    }
}
elsif($in{'appoint'} eq '' && $in{'delete'} ne ''){
    #予約を削除する場合
    #該当する予約をメモ帳から探す．
    my($deflag) = 0;
    foreach $tmp (@text){
        my @inappo = split(',', $tmp);
	if($inappo[0] eq $in{'dename'} && $inappo[1] == $in{'deday'} && 
	   $inappo[2] == $in{'dehour'} && $inappo[3] == $in{'dethirty'}){
	    $tmp = ''; #メモ帳がコピーされた配列の，当該箇所を削除
	    $deflag = 1;

	    #データを削除した配列を test.txt に書き出す
        open (OUT,"+< appointdata/data.txt");
	    flock(OUT, 2);
	    truncate(OUT, 0);
	    seek(OUT, 0, 0);
        print OUT @text;
        close (OUT);
	    last;
	}
    }

    if($deflag == 0){	
        $info = '該当する予約が存在しませんでした。';
    }else{
        $info = sprintf("%s%d時%d分から始まる， '%s' の予約を削除しました。", $sche[$in{'deday'}], $in{'dehour'}, 30 * $in{'dethirty'}, $in{'dename'});
        my($hist) = sprintf("%s%d時%d分から始まる， '%s'", $sche[$in{'deday'}], $in{'dehour'}, 30 * $in{'dethirty'}, $in{'dename'});
        &update_histry($hist, "削除");
    }
}
else{
    $info = '';
}

#以上のデータから表を作成
foreach $tmp (@text){
    my @indata = split(',', $tmp);
    if($indata[4] != 0){
        &add_appoint($indata[0], $indata[1], $indata[2], $indata[3], $indata[4], $indata[5], \@appdata);
    }
}

print "<center>";
print "<BR><BR>";
print "<font size = 7>";
print "●部室予\約表\●<BR>";
print "<font size = 5>";
if($info ne ''){
	$newinfo = "<BR>" . $info . "<BR>";
}else{
	$newinfo = '';
}
print "<font color = red>$newinfo<BR></Center>";

#実際に表を書き出す
print "<table align=center border=\"0\" cellspacing=0 >\n";

for($b = 0; $b <= 12; $b ++){
    print "<td height=30 colspan=2 align=center valign=center style=\"border-style:none;\"><font size=5>$b</td>\n";
}

for($a = 0; $a < 20; $a ++){
    print "</tr>\n";
    if($a % 2 == 0){
	#$tmps1 = substr($sche[$a/2],0, -3);
	#$tmps2 = substr($sche[$a/2],-3);
	$tmps1 = $schedate[$a/2];
	$tmps2 = $scheday[$a/2];
       print "<td height=$mheight width=60 rowspan=2 align=center valign=center style=\"border-style:none;\"><font size=5>$tmps1<BR>$tmps2</td>\n";
    }
    
    for($b = 0; $b < 24; $b ++){        
        print "$appdata[$a * 24 + $b]";
    }
    print "<td height=$mheight width=$mwidth style=\"border-width:thin; border-style:none;\">　　</td>\n";
    print "</tr>\n";
}

for($b = 0; $b <= 12; $b ++){
    print "<td height=30 colspan=2 align=center valign=center style=\"border-style:none;\"><font size=5>$b</td>\n";
}
print "</table>\n";


print <<"HTML";


<BR>
<form action="appoint.cgi" method="post">
<table align=center>
<tr>
<font size = 5>
<td valign= baseline style="border-style:ridge; word-break: break-all;">

<font size = 5>
<Center>予\約フォーム</Center><BR>
バンド名：<input type="text" name="name" size="20" style="font-size:20px"><BR><BR>
枠の色：
<select name="fcolor" style="font-size:20px">
<option value="0" style="background-color:#ffffff">お任せ</option>
<option value="1" style="background-color:#000000; color:#ffffff">■黒</option>
<option value="2" style="background-color:#808080">■グレー</option>
<option value="3" style="background-color:#c0c0c0">■シルバー</option>
<option value="4" style="background-color:#ffffff">■白</option>
<option value="5" style="background-color:#ff00ff; color:#ffffff">■ピンク</option>
<option value="6" style="background-color:#800080; color:#ffffff">■紫</option>
<option value="7" style="background-color:#800000; color:#ffffff">■栗色</option>
<option value="8" style="background-color:#ff0000; color:#ffffff">■赤</option>
<option value="9" style="background-color:#ffff00;">■黄</option>
<option value="10" style="background-color:#00ff00;">■ライム</option>
<option value="11" style="background-color:#008000;">■緑</option>
<option value="12" style="background-color:#008080;">■青緑</option>
<option value="13" style="background-color:#0000ff; color:#ffffff">■青</option>
<option value="14" style="background-color:#000080; color:#ffffff">■ネイビー</option>
<option value="15" style="background-color:#00ffff">■アクア</option>
<option value="16" style="background-color:#808000">■オリーブ</option>
</select>
<BR><BR>

HTML
&day_pulldown('day');
&hour_pulldown('hour', 'thirty');
print "　";
print "<BR><BR>";
&minutes_pulldown('minutes');
print "　予\約する。<BR><BR>";
print <<"HTML";

<span style="line-height:150%">予\約を入れる場合は，<BR>下のボタンを押してください。</span><BR><BR>
<input type="submit" name= "appoint" value="予\約確定" style="font-size:20px"><BR><BR>
</td>
<td width = 80>
</td>
<td valign= baseline style="border-style:ridge; word-break: break-all;">


<font size = 5>
<Center><font color = red>※<font color = black>削除フォーム<font color = red>※<font color = black></Center><BR>
HTML
&day_pulldown('deday');
&hour_pulldown('dehour', 'dethirty');
print "<BR><BR>";
print "予\約していた<BR><BR>";
print <<"HTML";
バンド名：<input type="text" name="dename" size="20" style="font-size:20px"><BR><BR>
の予\約を取り消す。<BR><BR>
<span style="line-height:150%"><font color = red>予\約を取り消す場合のみ，<BR>下のボタンを押してください。<font color = black></span><BR><BR>
<input type="submit" name= "delete" value="予\約を削除" style="font-size:20px"><BR><BR>
</td>
</tr>
</table>
<BR><BR>

<table align=center>
<tr>
<td width = 480 valign= baseline style="border-style:ridge; word-break: break-all;">
<span style="line-height:200%">
<font size = 3 color = black>
意見，不具合(正しく予\約できない，文字化け等）<BR>
などありましたら，ワルサーのLINEまでお願いします。<BR>
ページが読み込めない場合は，時間を置いた後に<BR>
一度更新してみてください。<BR>
</td>
</tr>
<table>


<center>
<BR><BR>
<a href="showhist.cgi">
履歴を表\示\する
</a>

<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
<p align=left>
<a href="walther_game.cgi">
w
</a>
</p>
</center>
<body>
</body>
HTML

exit;

#googleカレンダー
#<iframe src="https://www.google.com/calendar/embed?showPrint=0&amp;showCalendars=0&amp;height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=cusg5frn9q1nbu2na549havuqc%40group.calendar.google.com&amp;color=%2329527A&amp;ctz=Asia%2FTokyo" style=" border-width:0 " width="800" height="600" frameborder="0" scrolling="no">
#</iframe>

sub add_appoint{
    my($name, $day, $hour, $thirty, $minutes, $frame, $adata) = @_;
    my($snum) = ($day * 2) * 24 + $hour * 2 + $thirty;

    $framecolor = &num_to_color($frame);

    #11から13時とか，表が改行されるとこに予約が入ると，折り返すように二つ予約を作る
    #if(($hour * 2 + $thirty >= 21) && ($hour * 2 + $thirty <= 23) && $minutes > 1){
    #    my($hami) = $hour * 2 + $thirty + $minutes - 1 - 23;
    #    &add_appoint($name, $day, 12, 0, $hami, $frame, \@$adata); #再帰処理
    #    $minutes -= $hami;
    #}
    if(($hour * 2 + $thirty >= 21) && ($hour * 2 + $thirty <= 23) && ($hour * 2 + $thirty + ($minutes - 1) >= 24)){
    	my($hami) = $hour * 2 + $thirty + $minutes - 1 - 23;
        &add_appoint($name, $day, 12, 0, $hami, $frame, \@$adata); #再帰処理
        $minutes -= $hami;
    }
    
    my($fsize) = $minutes + 1;
    #my($len) = length($name);
    #できるだけ文字をでかくする封印中
    #if($fsize == 2){
    #	if($len <= 2){$fsize += 3;}
    #	elsif($len <= 4){$fsize += 2;}
    #}
    #elsif($fsize == 3){
    #	if($len <= 6){$fsize += 2;}
    #	elsif($len <= 8){$fsize += 1;}
    #}
    #elsif($fsize == 4){
    #	if($len <= 12){$fsize += 1;}
    #}
    
    $$adata[$snum] = "<td colspan=$minutes
                               height=$mheight width=$mwidth align=center 
                                style=\" border:4px ridge $framecolor; word-break: break-all;\">
                           <font size = $fsize color=\"#000000\">$name</td>\n";
    
    if($minutes > 1 && $minutes < 5){	  
        for(my($i)=1; $i < $minutes; $i ++){
            $$adata[$snum + $i] = '';
        }
    }
    
    if($snum != 23 && $snum != 47){
    	#$$adata[$snum + 1] =~ s/(?:break-all)/break-all; border-left-style:'none'/g;
    }
    
}

sub file_write_down{	
	my($filename, $text) = @_;
	open (OUT,"+< appointdata/$filename");
    flock(OUT, 2);
    truncate(OUT, 0);
    seek(OUT, 0, 0);
    print OUT \@$text;
    close (OUT);
}

sub update_histry{
	my($text, $pattern) = @_;
	
	my(@del) = ('から始まる\s', '，', '\sで');
	
	foreach $tmp(@del){
		$text =~ s/$tmp//g;
	}
	
	my($uptime) = time;
	($sec,$min,$hour,$mday,$mon,$year,$wno) = localtime($uptime);
	$outtext = sprintf("%02d/%02d,%02d:%02d:%02d,%s,%s\n", $mon + 1, $mday, $hour, $min, $sec, $pattern, $text);
	
	#ロックの関係で，インとアウトを分ける?
	open (IN, "appointdata/histry.txt");
	@lines = <IN>;
	#行数をカウント
	1 while <IN>;
	$count = $.;
	close (IN);
	unshift(@lines, $outtext);
	
	if($count >= 500){
		for(my($i) = 499; $i < $count; $i ++){
		    $lines[$i] = '';
		}
	}
			
	#ロック掛けずに運用してみる
	open (OUT,"+< appointdata/histry.txt");
	#flock(OUT, 2);
	#truncate(OUT, 0);
	seek(OUT, 0, 0);
    print OUT @lines;
    close (OUT);
}


sub num_to_applength{
    my($num) = @_;
    my($applen) = '';
    if($num == 1){$applen = '30分間';}
    if($num == 2){$applen = '1時間';}
    if($num == 3){$applen = '1時間30分';}
    if($num == 4){$applen = '2時間';}
    
    return $applen;
}
sub num_to_color{
    my($num) = @_;
    my($color);
    
    if($num == 0){
        $num = int(rand 15) + 1;
    }

    if($num == 1){$color = '#000000';}
    if($num == 2){$color = '#808080';}
    if($num == 3){$color = '#c0c0c0';}
    if($num == 4){$color = '#ffffff';}
    if($num == 5){$color = '#ff00ff';}
    if($num == 6){$color = '#800080';}
    if($num == 7){$color = '#800000';}
    if($num == 8){$color = '#ff0000';}
    if($num == 9){$color = '#ffff00';}
    if($num == 10){$color = '#00ff00';}
    if($num == 11){$color = '#008000';}
    if($num == 12){$color = '#008080';}
    if($num == 13){$color = '#0000ff';}
    if($num == 14){$color = '#000080';}
    if($num == 15){$color = '#00ffff';}
    if($num == 16){$color = '#808000';}
    return $color;
}

sub day_pulldown{
    my($dayname) = @_;

    print "<select name=\"$dayname\" style=\"font-size:20px\">";
    for(my($i)=0; $i < 10; $i ++){
        my($str) = sprintf("%s %s </option>", $day_selcted[$i], $sche[$i]);
        print "$str";
    }
    print "</select>";
    print "　に<BR><BR>";
}

sub hour_pulldown{
    my($hourname, $thirtyname) = @_;

    print "<select name=\"$hourname\" style=\"font-size:20px\">";
    for(my($i)=0; $i < 24; $i ++){     
	if($i == 8){
       	    $str = sprintf("<option value=%d selected>%d</option>", $i, $i);
	}else{
            $str = sprintf("<option value=%d>%d</option>", $i, $i);
	}
        print "$str";
    }
    print "</select>";
    print "　時　";
    
    print "<select name=\"$thirtyname\" style=\"font-size:20px\"><BR><BR>";
    print "<option value=\"0\">0</option>";
    print "<option value=\"1\">30</option>";
    print "</select>";
    print "　分から";
}


sub minutes_pulldown{
    my($minutesname) = @_;
    print "<select name=\"$minutesname\" style=\"font-size:20px\">";
    print "<option value=\"1\">30分</option>";
    print "<option value=\"2\">1時間</option>";
    print "<option value=\"3\">1時間30分</option>";
    print "<option selected value=\"4\">2時間</option>";
    print "</select>";
}

######################
######################
#
# To do
#
#
####################