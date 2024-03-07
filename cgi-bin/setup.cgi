#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/vpn.pl";

my $commandline = "";
my $setkey_tflag = &vpn::get_setkey_tflag();

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Location: ./general.cgi\n\n";
}

&hyper::get_args($commandline);			# 引数取得関数
#$commandline = "btnReset=1";
if ($commandline) {
	$commandline = &hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnReset", $commandline);
}

if ($setting ne "") {
	my @Values = values %hyper::cfg_name;

	foreach my $v (@Values) {
		my $file = &hyper::get_temp_file($v);
		if (-e $file) {
			my $cpfile = &hyper::get_modify_file($v);
			my @Buff = &hyper::readfile2($file);
			&hyper::writefile($cpfile, @Buff);
		}
	}
#	&appli::copyapplicationfolder;

#変更フラグを立てる
	my $flag = &hyper::get_flag_file($hyper::flag_name{'modify'});
	my @s = ("1");
	&hyper::writefile($flag, @s);

#RSA鍵の作成フラグを立てる
if( -f $setkey_tflag){
	my $flag = &hyper::get_flag_file($hyper::flag_name{'setkey'});
	my @s = ("1");
	&hyper::writefile($flag, @s);
}

#再起動フラグを立てる
	$flag = &hyper::get_flag_file($hyper::flag_name{'reboot'});
	&hyper::writefile($flag, @s);

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
total = 60;			// 読み込むトータル画像数
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

	progTitle.innerText = "再起動中";
	var kaisu = total-per;
	progMsg.innerText = "約"+kaisu+"秒後に再接続してください。";

	if (per == total) setTimeout("hideProgressBar()",1000);
	else setTimeout('progressBar()',1000);
}
//　１秒経過したらプログレスバーを消去
function hideProgressBar()
{
	progTitle.innerText = "再接続可能です。";
	document.all["progMsg"].style.visibility = "hidden";
	document.all["barBG"].style.visibility = "hidden";
}

// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="progressBar();">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
<H2 align="center">設定保存と再起動</H2>
<CENTER>
<P><DIV ID="progTitle"></DIV></P>
<P><DIV ID="progMsg"></DIV></P>
</CENTER>
<P><DIV ID="barBG"><DIV ID="bar"></DIV></DIV></P>
</BODY>
</HTML>
EOFRESTART

}
else {
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
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
<H2 align="center">設定保存と再起動</H2>
<FORM action="./setup.cgi" method="post">
<CENTER>
<P>各設定を保存し、本体を再起動します。</P>
<P>再起動には約60秒程度かかります。</P>
<P/>
<P><INPUT type="submit" name="btnReset" value="保存後再起動実行"></P>
</CENTER>
</FORM>
</BODY>
</HTML>
EOFHTML
}
