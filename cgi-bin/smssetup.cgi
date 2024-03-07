#!/usr/bin/perl -w

require "hyper.pl";

%item_smssetup = (
 'sms'              => "sms",
 'smsforce'         => "smsforce",
 'smssend'          => "smssend",
 'smsauthtype'      => "smsauthtype",
 'spppuser'         => "spppuser",
 'sppppasswd'       => "sppppasswd",
 'sdhcpdns1'        => "sdhcpdns1",
 'sdhcpdns2'        => "sdhcpdns2",

 'slcpecho'         => "slcpecho",
 'swanip'           => "swanip",
 'sremoteip'        => "sremoteip",
 'sidle_time'       => "sidle_time",
 'sconnecttime'     => "sconnecttime",
 'sapn'		    => "sapn",
 'spdp'		    => "spdp",
 'sdnscheck'	    => "sdnscheck",
 'sreceiveallow'    => "sreceiveallow",
 'sallownumber1'    => "sallownumber1",
 'sallownumber2'    => "sallownumber2",
 'sallownumber3'    => "sallownumber3",
 'sallownumber4'    => "sallownumber4",
 'sallownumber5'    => "sallownumber5",
 'sallownumber6'    => "sallownumber6",
 'sallownumber7'    => "sallownumber7",
 'sallownumber8'    => "sallownumber8",
 'sallownumber9'    => "sallownumber9",
 'sallownumber10'   => "sallownumber10",
);

%item_def_smssetup = (
 'sms'              => "0",
 'smsforce'         => "0",
 'smssend'          => "0",
 'smsauthtype'      => "2",
 'spppuser'         => "mopera",
 'sppppasswd'       => "pass",
 'sdhcpdns1'        => "220.159.212.200",
 'sdhcpdns2'        => "220.159.212.201",

 'slcpecho'          => "1",
 'swanip'           => "",
 'sremoteip'        => "",
 'sidle_time'       => "180",
 'sconnecttime'     => "600",
 'sapn'	            => "mopera.flat.foma.ne.jp",
 'spdp'		    => "IP",
 'sdnscheck'	    => "0",
 'sreceiveallow'    => "0",
 'sallownumber1'    => "",
 'sallownumber2'    => "",
 'sallownumber3'    => "",
 'sallownumber4'    => "",
 'sallownumber5'    => "",
 'sallownumber6'    => "",
 'sallownumber7'    => "",
 'sallownumber8'    => "",
 'sallownumber9'    => "",
 'sallownumber10'   => "",
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
 'apnerror'   => "接続先APNは半角英数字31文字以内で指定してください。",
 'telnumberseterror'   => "接続限定有効では接続許可電話番号を指定してください。",
 'telnumbererror'   => "接続許可電話番号は半角数字20文字以内で指定してください。",
);

my $section = 'smssetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $sreceiveallow_value ="";
my $sms_sel ="";
my $sms_force ="";
my $sms_send ="";
my $sms_pdp ="";
my $sms_dnscheck ="";
my $smsauth_type ="";
my $slcpecho_value ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_smssetup;
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

$sms_sel = input_sms($items{sms});

#$sms_force = input_smsforce($items{smsforce});
$sms_force = &set_radio3_pr("smsforce", $items{smsforce}, "0", "1", "2",  "通常接続", "強制接続", "コールバックのみ");
$smsauth_type = &set_radio4_pr("smsauthtype", $items{smsauthtype}, "2", "1", "0", "3",  "CHAP/PAP", "PAP", "CHAP", "認証無し");

$sreceiveallow_value = input_sreceiveallow($items{sreceiveallow});

$sms_send = input_smssend($items{smssend});
$sms_pdp = input_smspdp($items{spdp});
$sms_dnscheck = input_smsdnscheck($items{sdnscheck});
$slcpecho_value = input_slcpecho($items{slcpecho});

sub chk_item {
	my %items = @_;
=pod
	if (&hyper::chk_graph($items{telnumber}, 20) eq "" ) {
		return "telnumbererror";
	}
=cut

	if ($items{smsauthtype} ne "3") {
	if (($items{spppuser} eq "") or ($items{sppppasswd} eq "")) {
		return "autherror";
	}
	}

	if (&hyper::chk_graph($items{spppuser}, 64) eq "" ) {
		return "pppusererror";
	}

	if (&hyper::chk_graph($items{sppppasswd}, 20) eq "" ) {
		return "ppppasswderror";
	}

	if (($items{sdhcpdns1} eq "") and ($items{sdhcpdns2} ne "")) {
		return "dnserror_order";
	}
	elsif (($items{sdhcpdns1} ne "") and ($items{sdhcpdns2} ne "")) {
		if (&hyper::get_ipaddress($items{sdhcpdns1}) eq "") {
			return  "dnserror1";
		}
		if (&hyper::get_ipaddress($items{sdhcpdns2}) eq "") {
			return "dnserror2";
		}
		if ($items{sdhcpdns1} eq $items{sdhcpdns2}) {
			return "dnserror12";
		}
	}
	elsif ($items{sdhcpdns1} ne "") {
		if (&hyper::get_ipaddress($items{sdhcpdns1}) eq "") {
			return  "dnserror1";
		}
	}
	if ($items{swanip} ne "") {
		if (&hyper::get_ipaddress($items{swanip}) eq "") {
			return "waniprerror";
		}
	}
	if ($items{sremoteip} ne "") {
		if (&hyper::get_ipaddress($items{sremoteip}) eq "") {
			return "remoteiprerror";
		}
	}

	if (&hyper::checknumstring($items{sidle_time}) == 0) {
		return "idletimeinterror";
	}

	if (($items{sidle_time} < 10) || ($items{sidle_time} > 86400)) {
		return "idletimeerror";
	}

	if (&hyper::checknumstring($items{sconnecttime}) == 0) {
		return "connecttimeinterror";
	}

	if ($items{sconnecttime} != 0) {
		if (($items{sconnecttime} < 60) || ($items{sconnecttime} > 86400)) 		{
			return "connecttimeerror";
		}
	}

	if (&hyper::chk_graph($items{sapn}, 31) eq "" ) {
		return "apnerror";
	}

	if (($items{sreceiveallow} == 1) && (length $items{sallownumber1} == 0) && (length $items{sallownumber2} == 0) && (length $items{sallownumber3} == 0) && (length $items{sallownumber4} == 0) && (length $items{sallownumber5} == 0) && (length $items{sallownumber6} == 0) && (length $items{sallownumber7} == 0) && (length $items{sallownumber8} == 0) && (length $items{sallownumber9} == 0) && (length $items{sallownumber10} == 0)){
		return "telnumberseterror";
	}
	if (length $items{sallownumber1}) {
		if (($items{sallownumber1} !~ /^[0-9]+$/) || (length $items{sallownumber1} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber2}) {
		if (($items{sallownumber2} !~ /^[0-9]+$/) || (length $items{sallownumber2} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber3}) {
		if (($items{sallownumber3} !~ /^[0-9]+$/) || (length $items{sallownumber3} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber4}) {
		if (($items{sallownumber4} !~ /^[0-9]+$/) || (length $items{sallownumber4} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber5}) {
		if (($items{sallownumber5} !~ /^[0-9]+$/) || (length $items{sallownumber5} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber6}) {
		if (($items{sallownumber6} !~ /^[0-9]+$/) || (length $items{sallownumber6} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber7}) {
		if (($items{sallownumber7} !~ /^[0-9]+$/) || (length $items{sallownumber7} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber8}) {
		if (($items{sallownumber8} !~ /^[0-9]+$/) || (length $items{sallownumber8} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber9}) {
		if (($items{sallownumber9} !~ /^[0-9]+$/) || (length $items{sallownumber9} > 20)) {
			return "telnumbererror";
		}
	}
	if (length $items{sallownumber10}) {
		if (($items{sallownumber10} !~ /^[0-9]+$/) || (length $items{sallownumber10} > 20)) {
			return "telnumbererror";
		}
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

sub input_sms {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"sms\" value=\"0\" checked>無効 <INPUT type=\"radio\" name=\"sms\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"sms\" value=\"0\" >無効 <INPUT type=\"radio\" name=\"sms\" value=\"1\" checked>有効";
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

sub input_smsforce {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"smsforce\" value=\"0\" checked>無効 <INPUT type=\"radio\" name=\"smsforce\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"smsforce\" value=\"0\" >無効 <INPUT type=\"radio\" name=\"smsforce\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_sreceiveallow {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"sreceiveallow\" value=\"0\" checked>限定しない  <INPUT type=\"radio\" name=\"sreceiveallow\" value=\"1\">限定する";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"sreceiveallow\" value=\"0\" >限定しない  <INPUT type=\"radio\" name=\"sreceiveallow\" value=\"1\" checked>限定する";
	}
	return $p;
}

sub input_smssend {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"smssend\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"smssend\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"smssend\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"smssend\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_smspdp {
	my $v = $_[0];
	my $p;

	if ("$v" eq "IP") {
		$p = "<INPUT type=\"radio\" name=\"spdp\" value=\"IP\" checked>IP  <INPUT type=\"radio\" name=\"spdp\" value=\"PPP\">PPP(WCDMA固定)";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"spdp\" value=\"IP\" >IP  <INPUT type=\"radio\" name=\"spdp\" value=\"PPP\" checked>PPP(WCDMA固定)";
	}
	return $p;
}

sub input_smsdnscheck {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"sdnscheck\" value=\"0\" checked>指定しない  <INPUT type=\"radio\" name=\"sdnscheck\" value=\"1\">指定する";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"sdnscheck\" value=\"0\" >指定しない  <INPUT type=\"radio\" name=\"sdnscheck\" value=\"1\" checked>指定する";
	}
	return $p;
}

sub input_slcpecho {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"slcpecho\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"slcpecho\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"slcpecho\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"slcpecho\" value=\"1\" checked>有効";
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
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>SMS着信設定</H2>
<FORM name="smssetup" action="./smssetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>

<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">SMS着信</TD>
     <TD width="200">$sms_sel</TD>
    </TR>

    <TR>
      <TD>接続先APN</TD>
      <TD><INPUT type="text" name="sapn" size="31" maxlength="31" value="$items{sapn}" $readonly></TD>
    </TR>

    <TR>
     <TD width="200">PDP設定</TD>
     <TD width="200">$sms_pdp</TD>
    </TR>

    <TR>
     <TD width="200">閉域網利用指定</TD>
     <TD width="200">$sms_dnscheck</TD>
    </TR>

    <TR>
     <TD width="200">ipアドSMSコールバック</TD>
     <TD width="200">$sms_send</TD>
    </TR>

    <TR>
     <TD width="200">SMS着信動作</TD>
     <TD width="330">$sms_force</TD>
    </TR>

  </TBODY>
</TABLE>

<BR>
PPP設定
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="200">認証方式</TD>
      <TD width="330">$smsauth_type</TD>
    </TR>
    <TR>
      <TD>PPPユーザ名</TD>
      <TD><INPUT type="text" name="spppuser" size="31" maxlength="64" value="$items{spppuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>PPPパスワード</TD>
      <TD><INPUT type="password" name="sppppasswd" size="31" maxlength="20" value="$items{sppppasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>WAN側IPアドレス</TD>
      <TD><INPUT type="text" name="swanip" size="31" maxlength="15" value="$items{swanip}" $readonly></TD>
    </TR>
    <TR>
      <TD>リモートIPアドレス</TD>
      <TD><INPUT type="text" name="sremoteip" size="31" maxlength="15" value="$items{sremoteip}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNSサーバIP(プライマリ)</TD>
      <TD><INPUT type="text" name="sdhcpdns1" size="31" maxlength="15" value="$items{sdhcpdns1}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNSサーバIP(セカンダリ)</TD>
      <TD><INPUT type="text" name="sdhcpdns2" size="31" maxlength="15" value="$items{sdhcpdns2}" $readonly></TD>
    </TR>

    <TR>
      <TD>無通信監視時間</TD>
      <TD><INPUT type="text" name="sidle_time" size="31" maxlength="5" value="$items{sidle_time}" $readonly>秒</TD>
    </TR>
    <TR>
      <TD>強制切断時間</TD>
      <TD><INPUT type="text" name="sconnecttime" size="31" maxlength="5" value="$items{sconnecttime}" $readonly>秒</TD>
    </TR>
    <TR>
     <TD width="200">LCP-ECHO監視</TD>
     <TD width="200">$slcpecho_value</TD>
    </TR>
  </TBODY>
</TABLE>


<BR>
ジャンク着信リジェクト機能
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">接続限定</TD>
     <TD width="200">$sreceiveallow_value</TD>
    </TR>
    <TR>
      <TD>接続許可電話番号1</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber1" value="$items{sallownumber1}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号2</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber2" value="$items{sallownumber2}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号3</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber3" value="$items{sallownumber3}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号4</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber4" value="$items{sallownumber4}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号5</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber5" value="$items{sallownumber5}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号6</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber6" value="$items{sallownumber6}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号7</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber7" value="$items{sallownumber7}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号8</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber8" value="$items{sallownumber8}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号9</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber9" value="$items{sallownumber9}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続許可電話番号10</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber10" value="$items{sallownumber10}" $readonly></TD>
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
	%items = &hyper::get_section($section, "", \%item_smssetup, \%item_def_smssetup);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_smssetup;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_smssetup{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file($section);
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}


