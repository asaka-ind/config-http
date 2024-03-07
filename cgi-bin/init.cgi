#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

my $commandline = "";

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Location: ./general.cgi\n\n";
}

&hyper::get_args($commandline);			# 引数取得関数
#$commandline = "btnInit=1";
if ($commandline) {
	$commandline = &hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnInit", $commandline);
}

if ($setting ne "") {
#デフォルト設定フラグを立てる
	my $flag = &hyper::get_flag_file($hyper::flag_name{'default'});
	my @s = ("1");
	&hyper::writefile($flag, @s);

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

	progTitle.innerText = "初期化中";
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
<H2 align="center">初期化</H2>
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
<SCRIPT Language="JavaScript">
<!--
function MCheck() {
	return window.confirm("工場出荷時設定に戻します。よろしいですか？");
}
// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
<H2 align="center">初期化</H2>
<FORM action="./init.cgi" method="post" onSubmit="return MCheck()">
<CENTER>初期化を行うと、すべての設定が工場出荷値に戻ります。<BR>
<BR>
<INPUT type="submit" name="btnInit" value="初期化実行"><BR>
</CENTER>
</FORM>
</BODY>
</HTML>
EOFHTML
}
