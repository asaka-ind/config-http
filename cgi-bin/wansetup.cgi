#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_wansetup = (
 'pppuser'          => "pppuser",
 'ppppasswd'        => "ppppasswd",
 'dhcpdns1'         => "dhcpdns1",
 'dhcpdns2'         => "dhcpdns2",

 'wancheck'         => "wancheck",
 'carrier_id'       => "carrier_id",
 'lcpecho'          => "lcpecho",
 'authtype'         => "authtype",
 'connect'          => "connect",
 'keeppacket'       => "keeppacket",
 'wanip'            => "wanip",
 'remoteip'         => "remoteip",
 'idle_time'        => "idle_time",
 'connecttime'      => "connecttime",
 'apn'		    => "apn",
 'pdp'		    => "pdp",
 'dialicmp'	    => "dialicmp",
 'dialdns'	    => "dialdns",
 'dnscheck'	    => "dnscheck",
);

%item_def_wansetup = (
 'pppuser'          => "",
 'ppppasswd'        => "",
 'dhcpdns1'         => "",
 'dhcpdns2'         => "",

 'wancheck'         => "0",
 'carrier_id'       => "0",
 'lcpecho'          => "0",
 'connect'          => "1",
 'keeppacket'       => "0",
 'authtype'         => "3",
 'wanip'            => "",
 'remoteip'         => "",
 'idle_time'        => "180",
 'connecttime'      => "0",
 'apn'	            => "mopera.flat.foma.ne.jp",
 'pdp'	            => "IP",
 'dialicmp'	    => "1",
 'dialdns'	    => "1",
 'dnscheck'	    => "0",
);

%error_list = (
  'pppusererror'     => "発信ユーザ名は半角英数字64文字以内で指定してください。",
 'ppppasswderror'   => "発信パスワードは半角英数字20文字以内で指定してください。",
 'autherror'   => "認証有りではPPPユーザ名とPPPパスワードは空欄にしないでください。",
 'waniprerror'      => "WAN側IPアドレスの設定が正しくありません。",
 'remoteiprerror'   => "リモートIPアドレスの設定が正しくありません。",
 'idletimeinterror' => "無通信監視時間は整数で指定してください。",
 'idletimeerror'    => "無通信監視時間は10から86400秒の間で指定してください。",
 'connecttimeinterror' => "強制切断時間は整数で指定してください。",
 'connecttimeerror'    => "強制切断時間は0または60から86400秒の間で指定してください。",
 'dnserror_order'   => "DNSサーバIPはプライマリから指定してください。",
 'dnserror1'        => "DNSサーバIP(プライマリ)の設定が正しくありません。",
 'dnserror2'        => "DNSサーバIP(セカンダリ)の設定が正しくありません。",
 'dnserror12'       => "DNSサーバIP(プライマリ)とDNSサーバIP(セカンダリ)は異なるアドレスを指定してください。",
 'apnerror'   => "接続先(APN)は半角英数字39文字以内で指定してください。",
 'telnumberseterror'   => "接続先限定有効では接続許可電話番号を指定してください。",
 'telnumbererror'   => "接続許可電話番号は半角数字20文字以内で指定してください。",
);

my $section = 'wansetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $dialicmp_value ="";
my $dialdns_value ="";
my $dnscheck_value ="";
my $pdp_value ="";
my $connect_value ="";
my $lcpecho_value ="";
my $auth_type ="";
my $keep_packet ="";
my $wancheck_value ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_wansetup;
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

$keep_packet = input_keeppacket($items{keeppacket});

$dialicmp_value = input_dialicmp($items{dialicmp});

$dialdns_value = input_dialdns($items{dialdns});

$dnscheck_value = input_dnscheck($items{dnscheck});

$pdp_value = input_pdp($items{pdp});

$lcpecho_value = input_lcpecho($items{lcpecho});
$wancheck_value = input_wancheck($items{wancheck});
$connect_value = input_connect($items{connect});
#$connect_value = &set_radio3_pr("connect", $items{connect}, "0", "1", "2",  "常時接続", "イベント接続", "発信しない(SMSのみ）");
$auth_type = &set_radio4_pr("authtype", $items{authtype}, "3", "1", "2", "0",  "CHAP/PAP", "PAP", "CHAP", "認証無し");

sub chk_item {
	my %items = @_;

	if ($items{authtype} ne "0") {
	if (($items{pppuser} eq "") or ($items{ppppasswd} eq "")) {
		return "autherror";
	}
	}

	if (&hyper::chk_graph($items{pppuser}, 64) eq "" ) {
		return "pppusererror";
	}

	if (&hyper::chk_graph($items{ppppasswd}, 20) eq "" ) {
		return "ppppasswderror";
	}

	if (($items{dhcpdns1} eq "") and ($items{dhcpdns2} ne "")) {
		return "dnserror_order";
	}
	elsif (($items{dhcpdns1} ne "") and ($items{dhcpdns2} ne "")) {
		if (&hyper::get_ipaddress($items{dhcpdns1}) eq "") {
			return  "dnserror1";
		}
		if (&hyper::get_ipaddress($items{dhcpdns2}) eq "") {
			return "dnserror2";
		}
		if ($items{dhcpdns1} eq $items{dhcpdns2}) {
			return "dnserror12";
		}
	}
	elsif ($items{dhcpdns1} ne "") {
		if (&hyper::get_ipaddress($items{dhcpdns1}) eq "") {
			return  "dnserror1";
		}
	}
	if ($items{wanip} ne "") {
		if (&hyper::get_ipaddress($items{wanip}) eq "") {
			return "waniprerror";
		}
	}
	if ($items{remoteip} ne "") {
		if (&hyper::get_ipaddress($items{remoteip}) eq "") {
			return "remoteiprerror";
		}
	}

	if (&hyper::checknumstring($items{idle_time}) == 0) {
		return "idletimeinterror";
	}

	if (($items{idle_time} < 10) || ($items{idle_time} > 86400)) {
		return "idletimeerror";
	}

	if (&hyper::checknumstring($items{connecttime}) == 0) {
		return "connecttimeinterror";
	}

	if ($items{connecttime} != 0) {
		if (($items{connecttime} < 60) || ($items{connecttime} > 86400)) 		{
			return "connecttimeerror";
		}
	}

	if (&hyper::chk_graph($items{apn}, 39) eq "" ) {
		return "apnerror";
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


sub input_keeppacket {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"keeppacket\" value=\"0\" checked>維持パケット有り <INPUT type=\"radio\" name=\"keeppacket\" value=\"1\">維持パケット無し";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"keeppacket\" value=\"0\" >維持パケット有り <INPUT type=\"radio\" name=\"keeppacket\" value=\"1\" checked>維持パケット無し";
	}
	return $p;
}

sub input_dialicmp {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dialicmp\" value=\"0\" checked>許可しない <INPUT type=\"radio\" name=\"dialicmp\" value=\"1\">許可する";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dialicmp\" value=\"0\" >許可しない <INPUT type=\"radio\" name=\"dialicmp\" value=\"1\" checked>許可する";
	}
	return $p;
}

sub input_dialdns {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dialdns\" value=\"0\" checked>許可しない <INPUT type=\"radio\" name=\"dialdns\" value=\"1\">許可する";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dialdns\" value=\"0\" >許可しない <INPUT type=\"radio\" name=\"dialdns\" value=\"1\" checked>許可する";
	}
	return $p;
}

sub input_dnscheck {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dnscheck\" value=\"0\" checked>指定しない <INPUT type=\"radio\" name=\"dnscheck\" value=\"1\">指定する";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dnscheck\" value=\"0\" >指定しない <INPUT type=\"radio\" name=\"dnscheck\" value=\"1\" checked>指定する";
	}
	return $p;
}

sub input_pdp {
	my $v = $_[0];
	my $p;

	if ("$v" eq "IP") {
		$p = "<INPUT type=\"radio\" name=\"pdp\" value=\"IP\" checked>IP  <INPUT type=\"radio\" name=\"pdp\" value=\"PPP\">PPP(WCDMA固定)";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"pdp\" value=\"IP\" >IP  <INPUT type=\"radio\" name=\"pdp\" value=\"PPP\" checked>PPP(WCDMA固定)";
	}
	return $p;
}


sub input_connect {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"connect\" value=\"0\" checked>常時接続  <INPUT type=\"radio\" name=\"connect\" value=\"1\">イベント接続";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"connect\" value=\"0\" >常時接続  <INPUT type=\"radio\" name=\"connect\" value=\"1\" checked>イベント接続";
	}
	return $p;
}

sub input_wancheck {
        my $v = $_[0];
        my $p;

        if ("$v" eq "0") {
                $p = "<INPUT type=\"radio\" name=\"wancheck\" value=\"0\" checked>有効  <INPUT type=\"radio\" name=\"wancheck\" value=\"1\">無効";
        }
        else {
                $p = "<INPUT type=\"radio\" name=\"wancheck\" value=\"0\" >有効  <INPUT type=\"radio\" name=\"wancheck\" value=\"1\" checked>無効";
        }
        return $p;
}

sub input_lcpecho {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"lcpecho\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"lcpecho\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"lcpecho\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"lcpecho\" value=\"1\" checked>有効";
	}
	return $p;
}

sub set_radio3_pr{
	my ($name,$v,$value0,$value1,$value2,$va_pr0,$va_pr1,$va_pr2) = @_;
	my $p = "";
	my $checked0 = "";
	my $checked1 = "";
	my $checked2 = "";

	if("$v" eq "$value0"){
		$checked0 = "checked";
	}elsif("$v" eq "$value1"){
		$checked1 = "checked";
	}else{
		$checked2 = "checked";
	}
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0>$va_pr0 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1>$va_pr1 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value2\" $checked2>$va_pr2";
	
	return $p;
}

sub set_radio4_pr{
	my ($name,$v,$value0,$value1,$value2,$value3,$va_pr0,$va_pr1,$va_pr2,$va_pr3) = @_;
	my $p = "";
	my $checked0 = "";
	my $checked1 = "";
	my $checked2 = "";
	my $checked3 = "";

	if("$v" eq "$value0"){
		$checked0 = "checked";
	}elsif("$v" eq "$value1"){
		$checked1 = "checked";
	}elsif("$v" eq "$value2"){
		$checked2 = "checked";
	}else{
		$checked3 = "checked";
	}
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0>$va_pr0 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1>$va_pr1 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value2\" $checked2>$va_pr2";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value3\" $checked3>$va_pr3";
	return $p;
}


my $readonly ="";
my $disabled ="";
if (!&hyper::get_logincheck()) {
	$disabled = "disabled";
	$readonly = "readonly";
}


my $optcarrierid = &opt_carriersel($items{"carrier_id"});

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>WAN設定</H2>
<FORM name="wansetup" action="./wansetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>

<BR>
PPP設定
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">認証方式</TD>
     <TD width="330">$auth_type</TD>
    </TR>
    <TR>
      <TD>PPPユーザ名</TD>
      <TD><INPUT type="text" name="pppuser" size="31" maxlength="64" value="$items{pppuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>PPPパスワード</TD>
      <TD><INPUT type="password" name="ppppasswd" size="31" maxlength="20" value="$items{ppppasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>WAN側IPアドレス</TD>
      <TD><INPUT type="text" name="wanip" size="31" maxlength="15" value="$items{wanip}" $readonly></TD>
    </TR>
    <TR>
      <TD>リモートIPアドレス</TD>
      <TD><INPUT type="text" name="remoteip" size="31" maxlength="15" value="$items{remoteip}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNSサーバIP(プライマリ)</TD>
      <TD><INPUT type="text" name="dhcpdns1" size="31" maxlength="15" value="$items{dhcpdns1}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNSサーバIP(セカンダリ)</TD>
      <TD><INPUT type="text" name="dhcpdns2" size="31" maxlength="15" value="$items{dhcpdns2}" $readonly></TD>
    </TR>

    <TR>
      <TD>無通信監視時間</TD>
      <TD><INPUT type="text" name="idle_time" size="31" maxlength="5" value="$items{idle_time}" $readonly>秒</TD>
    </TR>
    <TR>
      <TD>強制切断時間</TD>
      <TD><INPUT type="text" name="connecttime" size="31" maxlength="5" value="$items{connecttime}" $readonly>秒</TD>
    </TR>
    <TR>
     <TD width="200">LCP-ECHO監視</TD>
     <TD width="200">$lcpecho_value</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
発信設定
<TABLE border="1">
  <TBODY>

<!--
    <TR>
     <TD width="200">キャリア</TD>
     <TD width="300">$optcarrierid</TD>
    </TR>
-->

    <TR>
     <TD width="200">接続方式</TD>
     <TD width="380">$connect_value</TD>
    </TR>

    <TR>
     <TD width="200">常時接続</TD>
     <TD width="300">$keep_packet</TD>
    </TR>

    <TR>
      <TD>接続先APN</TD>
      <TD><INPUT type="text" name="apn" size="39" maxlength="39" value="$items{apn}" $readonly></TD>
    </TR>

<!--
    <TR>
     <TD>PDP設定</TD>
     <TD>$pdp_value</TD>
    </TR>
-->

    <TR>
     <TD>ICMPプロトコルによる発信</TD>
     <TD>$dialicmp_value</TD>
    </TR>
    <TR>
     <TD>DNS(UDP:53)による発信</TD>
     <TD>$dialdns_value</TD>
    </TR>
    <TR>
     <TD>閉域網利用指定</TD>
     <TD>$dnscheck_value</TD>
    </TR>
    <TR>
     <TD width="200">接続監視</TD>
     <TD width="200">$wancheck_value</TD>
    </TR>
  </TBODY>
</TABLE>

</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %items = ();
	#g設定呼び出し
	%items = &hyper::get_section($section, "", \%item_wansetup, \%item_def_wansetup);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_wansetup;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_wansetup{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file($section);
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

sub opt_carriersel {
	my $value = $_[0];
	my @num   = ("1","2","3","4","5","6");
	my @type   = ("DoCoMo","KDDI","Softbank","FULL_MVNO","KDDI_MVNO","Softbank_MVNO");
	my $i;
	my $t;
	my $p = "<SELECT name=\"carrier_id\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=carrier_id value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=carrier_id value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

