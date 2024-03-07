#!/usr/bin/perl -w

require "hyper.pl";

my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
	$Readfile = &hyper::get_param("btnRead", $commandline);
	$Writefile = &hyper::get_param("btnWrite", $commandline);
}

if ($setting ne "") {

} elsif (defined $Readfile) {
	&set_fileout_item(%items);
	exit
} elsif (defined $Writefile) {
	&set_filein_item(\%items);
} else {
}

sub error_script {
	my $error = $error_list{$_[0]};
	my $pp = "<SCRIPT LANGUAGE=\"JavaScript1.1\">\n";

	$pp = $pp."<!---\n";
	$pp = $pp."window.alert(\"$error\")\n";
	$pp = $pp."//--->\n";
	$pp = $pp."</SCRIPT>\n";
	return $pp;
}

sub set_fileout_item {
	my %items = @_;

	$filedir='/etc/current.conf/';
	$filename='client.crt';
	$filepath=$filedir.$filename;

	my $default_name = "client.crt";
	print "Content-type: application/download\n";
	print "Content-disposition: attachment; filename=\"$default_name\"\n\n";
	open(IN,"$filepath");
	print <IN>;
	close(IN);
}

sub set_filein_item {
	my ($it) = @_;

	my $filename = "/tmp/client.crt.tmp";
	`mv /tmp/client.crt.tmp /etc/current.conf/client.crt`;
}

my $readonly ="";
my $disabled ="";
if (!&hyper::get_logincheck()) {
	$disabled = "disabled";
	$readonly = "readonly";
}

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css"></HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>クライアント証明書</H2>
<FORM action="./clicrtfile.cgi" method="post">

<BR>
クライアント証明書のファイル名はclient.crtとしてください。
<BR>
<BR>
クライアント証明書読出し
<BR>
<INPUT type="submit" name="btnRead" value="読出し">
<BR>
</FORM>
<form action="./clicrtload.cgi" enctype="multipart/form-data" method="post">
<BR>
クライアント証明書登録
<BR>
<input name="confFile" type="file" size="50" accept="application/octet-stream">
<BR>
<INPUT type="submit" name="btnWrite" value="書込み">
</FORM>
</BODY>
</HTML>
EOFHTML
