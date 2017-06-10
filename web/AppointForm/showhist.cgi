#!/usr/bin/perl

require 'jcode.pl';


print "Content-type: text/html; charset=UTF-8\n\n";
#print "Content-type: text/html; charset=Shift_JIS\n\n";

#文字化け対策のおまじない
print "<!-- \xfd\xfe(MOJIBAKE TAISAKU)-->\n";
print "<!-- 龠(MOJIBAKE TAISAKU) -->\n";

#ファイルを読み込み、配列に入れる。
open (IN, "appointdata/histry.txt");
@text = <IN>;
close (IN);

#アクセスのたびにバックアップを作成
open (OUT,"+> ../backup/histry_back.txt");
#flock(OUT, 2);
#truncate(OUT, 0);
seek(OUT, 0, 0);
print OUT @text;
close (OUT);
#表示

print "<center>";
print "<span style=\"line-height:120%\">";
print "<a href=\"appoint.cgi\">";
print "予\約表\へ戻る";
print "</a><BR><BR><BR>";
print"過去500件の投稿を表\示します。<BR><BR>";
print "</center>";

print "<table align=center border=\"1\" cellspacing=0 >\n";
print "<tr align=center>";
print "<th  style = \"border-width:thin; border-style:solid;\">　投稿日　</td>";
print "<th  style = \"border-width:thin; border-style:solid;\">　投稿時間　</td>";
print "<th  style = \"border-width:thin; border-style:solid;\">　種類　</td>";
print "<th  style = \"border-width:thin; border-style:solid;\">　投稿内容　</td>";
print "</tr>";
foreach $tmp (@text){
    my @intext = split(',', $tmp);
    
    print "<tr>";
    print "<td  align=center style = \"border-width:thin; border-style:solid;\">$intext[0]</td>";
    print "<td  align=center style = \"border-width:thin; border-style:solid;\">$intext[1]</td>";
    print "<td  align=center style = \"border-width:thin; border-style:solid;\">$intext[2]</td>";
    print "<td  style = \"border-width:thin; border-style:solid;\">$intext[3]</td>";
    print "</tr>";
}
print "</table>";
