#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Location: ./general.cgi\n\n";
}

my $readonly ="";
my $disabled ="";
my $section = 'log_get';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
#my $logfile = "./ramdisk/logfile";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

my $fnum = 0;
my $fnum_f = 9;
my @logdata = "";
my @logdata_f = "";
my @logdata_l = "";
my $max_lines = 100;

open(IN, "</home/log/logno");
$fnum = <IN>;
close(IN);
	
#`/opt/sbin/sudo chmod a+r /etc/log/hl210log`;
#`grep -e diald -e DANTE: -e syslogd /var/log/messages.old > /var/log/hl210log`;
#`grep -e diald -e DANTE: -e syslogd /var/log/messages >> /var/log/hl210log`;

open(IN, "</home/log/logfile$fnum");
#open(IN, "</etc/log/hl210log");
@logdata_l = <IN>;
close(IN);

my $lines = @logdata;
if($lines < $max_lines){
	if($fnum > 0){
		$fnum_f = $fnum -1;
	}
	if( -f "/home/log/logfile$fnum_f"){
		open(IN, "</home/log/logfile$fnum_f");
		@logdata_f = <IN>;
		close(IN);
	}
}

@logdata = (@logdata_f, @logdata_l);

sub get_txt_buf {
	my $pr = "<pre>";
	my $pe = "</pre>";
	$lines = @logdata;
	my $dt = "";
	my $i = 0;

	if($lines > $max_lines){
		$i = $lines - $max_lines;
	}

	for(; $i < $lines; $i++){
		$pr = $pr.$logdata[$i];
	}
	$pr = $pr.$pe;
	return $pr;
}

my $log_data = &get_txt_buf();


print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<META http-equiv="Content-Type" content="text/html; charset=EUC-jp">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 10.0.1.0 for Windows">
<title>動作ログ</title>
<!--
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
-->
<style type="text/css">
table{
 border-collapse:collapse;
 background:white;
}
td{
 border:1px solid #555555;
 padding:3px;
}
</style>
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item

<body>

<h2>動作ログ</h2>

<FORM action="./log_dl.cgi" method="post">
<INPUT type="submit" name="btnSend" value="ログ読み出し" $disabled>
$pr
<p>
<TABLE width="600" height="30">
  <TBODY>
    <TR>
      <TD>
      $log_data
     </TD>
   </TR>
  </TBODY>
</TABLE>
</form>
</body>
</html>
EOFHTML
