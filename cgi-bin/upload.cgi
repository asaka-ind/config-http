#!/usr/bin/perl -w
###! /usr/local/bin/perl

require "hyper.pl";

%error_list = (
 '1'  => 'ファイルが読み込めません。',
 '2'  => 'アップデート情報(キーサイズ)に誤りがあります。',
 '3'  => 'インストールタイプと違うタイプのアップデートファイルを指定しました。',
 '4'  => 'アップデートに失敗しました。',
 '5'  => '現在のバージョンより古いバージョンを指定しました。',
 '99' => '予期せぬエラーが発生しました。',
);

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
}

# カスタマイズパラメータ
$upload_dir = "/mnt/ramdisk";  # アップロードファイルを格納するディレクトリ
$state_file = "dl_file.status"; # download file status
$log_files = "/tmp/log*";

$ret = 0;

# 標準入力からデータを読みだす
$buf = "";
$len = 0;
$read_data = "";
$remain = $ENV{'CONTENT_LENGTH'};
$totalsize = 0;
$totalsize = $remain;
binmode(STDIN);
  $len = sysread(STDIN, $buf, 1024);
  die "read error: $filename" unless defined $len;
  if (!$len) {
    $ret = 1;
    goto DONE_STATE;
  }
  $remain -= $len;
  $read_data = $buf;
  $size = $len;
# データを解釈する
$pos1 = 0; # ヘッダ部の先頭
$pos2 = 0; # ボディ部の先頭
$pos3 = 0; # ボディ部の終端
$delimiter = "";

  # ヘッダ処理
  $pos2 = index($read_data, "\r\n\r\n", $pos1) + 4;
  @headers = split("\r\n", substr($read_data, $pos1, $pos2 - $pos1));
  $filename = "";
  $name = "";
  foreach (@headers) {
    if ($delimiter eq "") {
      $delimiter = $_;
    } elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"/i) {
      if ($3) {
        $filename = $3;
        if ($filename =~ /([^\\\/]+)$/) {
          $filename = $1;
        }
      }
    } elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"/i) {
      $name = $2;
    }
  }

  # download file header
  $ps1 = $pos2; # ヘッダ部の先頭
  $ps2 = 0; # file name end
  $head_size = 28;
  $filename_d = "";
  $filesize = 0;
  $readlen = 0;
  $ps2 = index($read_data, "\0", $ps1);
  if($ps2 - $ps1 > $head_size){
    $ret = 3;
    goto DONE_STATE;
  }
  $filename_d = substr($read_data, $ps1, $ps2 - $ps1);
#  if($filename_d ne $filename){
#    $ret = 3;
#    goto DONE_STATE;
#  }
  if($filename_d !~ /^HL3\w+.bin/ and $filename_d !~ /^\w+.bin/){
    $ret = 3;
    goto DONE_STATE;
  }
  $filesize = vec(substr($read_data, $ps1 + 24, 4), 0,32);
  if($filesize > $totalsize){
    $ret = 3;
    goto DONE_STATE;
  }
#ファイルを削除 090924
 	`rm $upload_dir/*`;
  open(STFILE, "> $upload_dir/$state_file");
      binmode(STFILE);
      print STFILE substr($read_data, $pos2, $head_size);
#      print STFILE sprintf("total size = %lX\n",$totalsize);
#      print STFILE sprintf("dlfile size = %lX\n",$filesize);
  close(STFILE);

  $pos2 += $head_size;

  # ボディ処理
  $pos3 = index($read_data, "\r\n$delimiter", $pos2);
  if($pos3 != -1){
        $size = $pos3 - $pos2;
  }else{
        $size -= $pos2;
  }
  if ($filename_d) {
    if (open(OUT, "> $upload_dir/$filename_d")) {
      binmode(OUT);
      print OUT substr($read_data, $pos2, $size);
    }
  } else {
    $ret = 1;
    goto DONE_STATE;
  }

  $readlen = $filesize - $size;
my $block = 16384;
while ($readlen > $block) {
  $len = sysread(STDIN, $buf, $block);
  die "read error: $filename" unless defined $len;
  last if $len == 0;
  $remain -= $len;
  $readlen -= $len;
   print OUT $buf;
}
while ($readlen) {
  $len = sysread(STDIN, $buf, $readlen);
  die "read error: $filename" unless defined $len;
  last if $len == 0;
  $remain -= $len;
  $readlen -= $len;
   print OUT $buf;
}
while ($remain) {
  $len = sysread(STDIN, $buf, $remain);
  die "read error: $filename" unless defined $len;
  last if $len == 0;
  $remain -= $len;
}
close(OUT);

$size = -s "$upload_dir/$filename_d";
if($size != $filesize){
	$ret = 4;
	goto DONE_STATE
}

DONE_STATE:{

while ($len) {
	$len = sysread(STDIN, $buf, 16384);
  	die "read error: $filename" unless defined $len;
}

if ($ret > 0) {
	if ($ret > 5) {
	# エラー情報が無い場合
 		$ret = 99;
	}
#ファイルを削除
 	unlink "$upload_dir/$filename_d";

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
</HEAD>
<BODY bgcolor="#cccccc">
<H2 align="center">バージョンアップ</H2>
<FORM action="./versionup.cgi">
<CENTER>
<P>バージョンアップファイルが正しくありません</P>
<P>$error_list{$ret}</P>
<P/>
<P><INPUT type="submit" name="btnReset" value="戻る"></P>
</CENTER>
</FORM>
</BODY>
</HTML>
EOFHTML

}
else {

print "Content-Type:text/html\r\n\r\n";
print <<EOFRESTART;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<STYLE TYPE="text/css">
<!--
#barBG { position:absolute;left:0px; font-size:4px;
         background-color:#d0d0d0; width:210px; height:32px;}
#bar   { position:absolute;left:5px; font-size:4px;
         background-color:#808080; width:0px;   height:22px; }
#progTitle {}
#progMsg {}
--></STYLE>
<SCRIPT Language="JavaScript">
<!--
// プログレスバー表示
per   = 0;			// パーセンテージ
total = 190;			// 読み込むトータル画像数
//#barWidth = 200;	// プログレスバーの横幅
function progressBar()
{
	wid = document.body.clientWidth;
	barWidth = wid-20;
	document.all["barBG"].style.width = barWidth+10;

	per++;
	w = (per / total) * barWidth;
	document.all["bar"].style.top   = document.all["barBG"].style.top+5;
	document.all["bar"].style.width = w;

	progTitle.innerText = "アップデート処理中";
	var kaisu = total-per;
	progMsg.innerText = "約"+kaisu+"秒後に再接続してください。";

	if (per == total) setTimeout("hideProgressBar()",1000);
	else setTimeout('progressBar()',1000);
}
//　１秒経過したらプログレスバーを消去
function hideProgressBar()
{
	progTitle.innerText = "アップデートが終了しました。";
	progMsg.innerText = "LEDを確認して再接続してください。";

	document.all["barBG"].style.visibility = "hidden";
}

// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="progressBar();">
<H2 align="center">バージョンアップ</H2>
<CENTER>
<P><DIV ID="progTitle"></DIV></P>
<P><DIV ID="progMsg"></DIV></P>
</CENTER>
<P><DIV ID="barBG"><DIV ID="bar"></DIV></DIV></P>
</BODY>
</HTML>
EOFRESTART

#my $ret = `/opt/sbin/do_verup &`;

#変更フラグを立てる
	#V104 091019
        `echo 1 > /dev/hl320_module_cnt`;
	`rm $log_files`;
	`sync`;
my $flag = &hyper::get_flag_file($hyper::flag_name{'update'});
my @s = ("1");
&hyper::writefile($flag, @s);

#再起動フラグを立てる
#$flag = &hyper::get_flag_file($hyper::flag_name{'reboot'});
#&hyper::writefile($flag, @s);
}
}
