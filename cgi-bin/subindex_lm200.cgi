#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

&hyper::get_logincheck(); 

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 10.0.3.0 for Windows">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>セットアップ</TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<FRAMESET rows="92,*">
  <FRAME name="top" src="../html/headname_lm200.html">
  <FRAMESET cols="203,*">
    <FRAME name="left" src="../cgi-bin/menu.cgi">
    <FRAME name="right" src="../cgi-bin/general.cgi">
  </FRAMESET>
  <NOFRAMES>
  <BODY>
  <P>このページを表示するには、フレームをサポートしているブラウザが必要です。</P>
  </BODY>
  </NOFRAMES>
</FRAMESET>
</HTML>
EOFHTML

