#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

my $commandline = "";

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
}

# 091001 kill upload.cgi
`killall upload.cgi`;

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
<H2>バージョンアップ</H2>
<form action="./upload.cgi" enctype="multipart/form-data" method="post">
<p>バージョンアップファイルを指定してください。</p>
<input name="File" type="file" size="50" accept="application/octet-stream">
<p>
<input name="btnSnd" type="submit" size="50"  value="送信"><br>
</p>
</form>
</body>
</html>
EOFHTML

