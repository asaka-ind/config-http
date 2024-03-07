#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_serial = (
 'serial'     => "serial",
 'macadr1' => "macadr1",
);

%item_network = (
 'ipadr1'     => "ipadr1",
 'subnetadr1' => "subnetadr1",
 'configport' => "configport",
 'wanconfig'  => "wanconfig",
);

%item_list = (%item_serial, %item_network);

%item_def = (
 'serial'     => "",
 'macadr1'    => "00:10:B8:00:00:01",
 'ipadr1'     => "192.168.1.1",
 'subnetadr1' => "255.255.255.0",
 'configport' => "80",
 'wanconfig'  => "ACCEPT",
);

%error_list = (
 'ipadrerror'     => "IPアドレスの設定が正しくありません。",
 'subnetadrerror' => "サブネットマスクの設定が正しくありません。",
 'portinterror'   => "ポート番号は整数で指定してください。",
 'porterror'      => "ポート番号は1から65535の範囲で指定してください。",
);

my $section = 'network';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $wanconfig_value ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_network;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);
	}
}
else {
	%items = &get_item();
}

sub get_item {
	my %items = ();
	my $i;

	#general呼び出し
	%items = &hyper::get_section($section, "", \%item_network, \%$item_def);

	#シリアルファイルを読み出す
	my $filename = &hyper::get_fix_file(".serial");
	&hyper::add_section($filename, "", \%items, \%item_serial);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_network;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file($section);
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

sub set_config_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_network;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_config_file($section);
	&hyper::writefile_hush($filename, \%rhash);
}

sub fin_item {
	my %items =();

	%items = &get_item();
	&set_config_item(%items);
	&clear_modify();
}

sub clear_modify {
	my $filename = &hyper::get_temp_file($section);
	if (-e $filename) {
		unlink($filename);
	}
}

sub chk_item {
	my %items = @_;

	if (&hyper::get_ipaddress($items{ipadr1}) eq "") {
		return "ipadrerror";
	}
	if (&hyper::get_submask($items{subnetadr1}) eq "") {
		return "subnetadrerror";
	}
	if (&hyper::checknumstring($items{configport}) == 0) {
		return "portinterror";
	}
	if (($items{configport} < 1) || ($items{configport} > 65535) || ($items{configport} == 23)) {
		return "porterror";
	}
	return "";
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

$wanconfig_value = input_wanconfig($items{wanconfig});

sub input_wanconfig {
	my $v = $_[0];
	my $p;

	if ("$v" eq "DROP") {
		$p = "<INPUT type=\"radio\" name=\"wanconfig\" value=\"ACCEPT\" >許可  <INPUT type=\"radio\" name=\"wanconfig\" value=\"DROP\" checked>拒否";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"wanconfig\" value=\"ACCEPT\" checked>許可  <INPUT type=\"radio\" name=\"wanconfig\" value=\"DROP\">拒否";
	}
	return $p;
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
<H2>ネットワーク設定</H2>
<FORM action="./network.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD colspan="2">LAN</TD>
    </TR>
    <TR>
      <TD>MACアドレス</TD>
      <TD>$items{macadr1}</TD>
    </TR>
    <TR>
      <TD>IPアドレス</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="ipadr1" value="$items{ipadr1}" $readonly></TD>
    </TR>
    <TR>
      <TD>サブネットマスク</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="subnetadr1" value="$items{subnetadr1}" $readonly></TD>
    </TR>
    <TR>
      <TD>設定ポート番号</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="configport" value="$items{configport}" $readonly></TD>
    </TR>
    <TR>
     <TD>WAN側からの設定</TD>
     <TD>$wanconfig_value</TD>
    </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML
