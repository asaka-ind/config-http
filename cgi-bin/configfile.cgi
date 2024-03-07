#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

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
	$filename='lm200_conf.tar';
	$filepath=$filedir.$filename;

	my $default_name = "lm200_conf.tar";
	print "Content-type: application/download\n";
	print "Content-disposition: attachment; filename=\"$default_name\"\n\n";
	open(IN,"$filepath");
	print <IN>;
	close(IN);
}

sub set_filein_item {
	my ($it) = @_;

	my $filename = "/tmp/lm200_conf.tar.tmp";
	`mkdir /tmp/config_tmp`;
	`mv /tmp/lm200_conf.tar.tmp /tmp/config_tmp/`;
	`tar -vx -f /tmp/config_tmp/lm200_conf.tar.tmp -C /tmp/config_tmp/`;
	`rm -f /tmp/config_tmp/lm200_conf.tar.tmp`;
	`cp /tmp/config_tmp/ddnssetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/dhcpsetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/etcsetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/etcsetup2 /etc/temp.conf/`;
	`cp /tmp/config_tmp/rssetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/rsstatussetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/filtersetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/general /etc/temp.conf/`;
	`cp /tmp/config_tmp/network /etc/temp.conf/`;
	`cp /tmp/config_tmp/password /etc/temp.conf/`;
	`cp /tmp/config_tmp/rsapubkey /etc/temp.conf/`;
	`cp /tmp/config_tmp/newkey /etc/temp.conf/`;
	`cp /tmp/config_tmp/ntpsetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/smssetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/snatsetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/vpnsetup /etc/temp.conf/`;
	`cp /tmp/config_tmp/wansetup /etc/temp.conf/`;
        `cp /tmp/config_tmp/mqttpubsetup /etc/temp.conf/`;
        `cp /tmp/config_tmp/mqttsendsetup /etc/temp.conf/`;
        `cp /tmp/config_tmp/ca.crt /etc/temp.conf/`;
        `cp /tmp/config_tmp/client.crt /etc/temp.conf/`;
        `cp /tmp/config_tmp/private.key /etc/temp.conf/`;
        `cp /tmp/config_tmp/mqtt_lognum /etc/temp.conf/`;
	`rm -rf /tmp/config_tmp/*`;	
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
<H2>全設定ファイル</H2>
<FORM action="./configfile.cgi" method="post">

<BR>
全設定ファイル一括取込み
<BR>
<INPUT type="submit" name="btnRead" value="読出し">
<BR>
</FORM>
<form action="./configload.cgi" enctype="multipart/form-data" method="post">
<BR>
全設定ファイル一括書込み
<BR>
<input name="confFile" type="file" size="50" accept="application/octet-stream">
<BR>
<INPUT type="submit" name="btnWrite" value="書込み">
</FORM>
</BODY>
</HTML>
EOFHTML
