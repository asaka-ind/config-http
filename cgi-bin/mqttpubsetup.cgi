#!/usr/bin/perl -w

require "hyper.pl";

%item_mqttpubsetup = (
 'pubon'	    => "pubon",
 'protocol'	    => "protocol",
 'authon'	    => "authon",
 'pubuser'          => "pubuser",
 'pubpasswd'        => "pubpasswd",
 'brokerip'         => "brokerip",
 'qos'     	    => "qos",
 'topic'  	    => "topic",
 'retain'	    => "retain",
 'pubid'            => "pubid",
 'mqttport'         => "mqttport",
 'keepalive'        => "keepalive",
 'clientcrt'        => "clientcrt",
 'willon'	    => "willon",
 'willtopic'	    => "willtopic",
 'willqos'	    => "willqos",
 'willretain'	    => "willretain",
 'willmessage'	    => "willmessage",
 'mqttver'          => "mqttver",
 'tlsver'           => "tlsver",
);

%item_def_mqttpubsetup = (
 'pubon'	    => "0",
 'protocol'	    => "0",
 'authon'	    => "0",
 'pubuser'          => "",
 'pubpasswd'        => "",
 'brokerip'         => "",
 'qos'  	    => "0",
 'topic'            => "",
 'retain'	    => "0",
 'pubid'            => "",
 'mqttport'         => "8883",
 'keepalive'        => "600",
 'clientcrt'        => "0",
 'willon'	    => "0",
 'willtopic'	    => "",
 'willqos'	    => "0",
 'willretain'	    => "0",
 'willmessage'	    => "",
 'mqttver'          => "1",
 'tlsver'           => "2",
);

%error_list = (
 'pubusererror'     => "認証ユーザ名は半角英数字128文字以内で指定してください。",
 'pubpasswderror'   => "認証パスワードは半角英数字256文字以内で指定してください。",
 'iperror'        => "接続先の設定が正しくありません。",
 'topicerror'   => "TOPICは半角英数字128文字以内で指定してください。",
 'pubautherror'   => "認証ユーザ名、認証パスワードを指定してください。",
 'pubiderror'     => "クライアントIDは半角英数字128文字以内で指定してください。",
 'willmeserror'     => "Willメッセージは半角英数字128文字以内で指定してください。",
 'portinterror'   => "ポート番号は整数で指定してください。",
 'porterror'      => "ポート番号は1から65535の範囲で指定してください。",
 'keepaliveinterror'   => "キープアライブは整数で指定してください。",
 'keepaliveerror'      => "キープアライブは2から65535の範囲で指定してください。",
);

my $section = 'mqttpubsetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $pubon_value ="";
my $protocol_value ="";
my $clientcrt_value ="";
my $authon_value ="";
my $retain_value ="";
my $mqttver_value ="";
my $qos_type ="";
my $willon_value ="";
my $willretain_value ="";
my $willqos_type ="";
my $tlsver_type ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_mqttpubsetup;
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

$pubon_value = input_pubon($items{pubon});

$protocol_value = input_protocol($items{protocol});

$clientcrt_value = input_clientcrt($items{clientcrt});

$authon_value = input_authon($items{authon});

$retain_value = input_retain($items{retain});

$mqttver_value = input_mqttver($items{mqttver});

$qos_type = &set_radio3_pr("qos", $items{qos}, "0", "1", "2",  "0", "1", "2");

$willon_value = input_willon($items{willon});

$willretain_value = input_willretain($items{willretain});

$willqos_type = &set_radio3_pr("willqos", $items{willqos}, "0", "1", "2",  "0", "1", "2");

$tlsver_type = &set_radio3_pr("tlsver", $items{tlsver}, "0", "1", "2",  "1", "1.1", "1.2");

sub chk_item {
	my %items = @_;

	if ($items{authon} ne "0") {
		if (($items{pubuser} eq "") or ($items{pubpasswd} eq "")) {
			return "pubautherror";
		}
	}

	if (&hyper::chk_graph2($items{pubuser}, 128) eq "" ) {
		return "pubusererror";
	}

	if (&hyper::chk_graph2($items{pubpasswd}, 256) eq "" ) {
		return "pubpasswderror";
	}

	if ($items{pubon} ne "0") {
		if (($items{brokerip} eq "") or (&hyper::chk_graph($items{brokerip}, 128) eq "")) {
			return  "iperror";
		}
	}

	if ($items{pubon} ne "0") {
		if (($items{topic} eq "") or (&hyper::chk_graph($items{topic}, 128) eq "" )) {
			return "topicerror";
		}
	}

	if (&hyper::chk_graph2($items{pubid}, 128) eq "" ) {
		return "pubiderror";
	}

        if (&hyper::checknumstring($items{mqttport}) == 0) {
                return "portinterror";
        }
        if (($items{mqttport} < 1) || ($items{mqttport} > 65535)) {
                return "porterror";
        }
        if (&hyper::checknumstring($items{keepalive}) == 0) {
                return "keepaliveinterror";
        }
        if (($items{keepalive} < 2) || ($items{keepalive} > 65535)) {
                return "keepaliveerror";
        }

	if ($items{willon} ne "0") {
		if (($items{willtopic} eq "") or (&hyper::chk_graph($items{willtopic}, 128) eq "" )) {
			return "topicerror";
		}
	}

	if (&hyper::chk_graph2($items{willmessage}, 128) eq "" ) {
		return "willmeserror";
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

sub input_pubon {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"pubon\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"pubon\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"pubon\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"pubon\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_willon {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"willon\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"willon\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"willon\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"willon\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_authon {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"authon\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"authon\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"authon\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"authon\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_protocol {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"protocol\" value=\"0\" checked>MQTTS(暗号化)  <INPUT type=\"radio\" name=\"protocol\" value=\"1\">MQTT";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"protocol\" value=\"0\" >MQTTS(暗号化)  <INPUT type=\"radio\" name=\"protocol\" value=\"1\" checked>MQTT";
	}
	return $p;
}

sub input_clientcrt {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"clientcrt\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"clientcrt\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"clientcrt\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"clientcrt\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_retain {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"retain\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"retain\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"retain\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"retain\" value=\"1\" checked>有効";
	}
	return $p;
}

sub input_mqttver {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"mqttver\" value=\"0\" checked>3.1  <INPUT type=\"radio\" name=\"mqttver\" value=\"1\">3.1.1";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"mqttver\" value=\"0\" >3.1  <INPUT type=\"radio\" name=\"mqttver\" value=\"1\" checked>3.1.1";
	}
	return $p;
}

sub input_willretain {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"willretain\" value=\"0\" checked>無効  <INPUT type=\"radio\" name=\"willretain\" value=\"1\">有効";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"willretain\" value=\"0\" >無効  <INPUT type=\"radio\" name=\"willretain\" value=\"1\" checked>有効";
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
<H2>MQTTパブリッシャー設定</H2>
<FORM name="mqttpubsetup" action="./mqttpubsetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>


<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD>パブリッシャー機能</TD>
     <TD>$pubon_value</TD>
    </TR>
    <TR>
     <TD>プロトコル</TD>
     <TD>$protocol_value</TD>
    </TR>
    <TR>
      <TD>ポート番号</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="mqttport" value="$items{mqttport}" $readonly></TD>
    </TR>
    <TR>
      <TD>接続先ブローカー</TD>
      <TD><INPUT type="text" name="brokerip" size="80" maxlength="128" value="$items{brokerip}" $readonly></TD>
    </TR>
    <TR>
      <TD>Topic</TD>
      <TD><INPUT type="text" name="topic" size="80" maxlength="128" value="$items{topic}" $readonly></TD>
    </TR>
    <TR>
     <TD width="200">QoS</TD>
     <TD width="230">$qos_type</TD>
    </TR>
    <TR>
     <TD>ユーザ名/パスワード認証</TD>
     <TD>$authon_value</TD>
    </TR>
    <TR>
      <TD>　ユーザ名</TD>
      <TD><INPUT type="text" name="pubuser" size="80" maxlength="128" value="$items{pubuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>　パスワード</TD>
      <TD><INPUT type="password" name="pubpasswd" size="80" maxlength="256" value="$items{pubpasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>クライアントID</TD>
      <TD><INPUT type="text" name="pubid" size="80" maxlength="128" value="$items{pubid}" $readonly></TD>
    </TR>
    <TR>
      <TD>キープアライブ(MQTT-PING)</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="keepalive" value="$items{keepalive}" $readonly>秒</TD>
    </TR>
    <TR>
     <TD>Retain</TD>
     <TD>$retain_value</TD>
    </TR>
    <TR>
     <TD>クライアント証明書</TD>
     <TD>$clientcrt_value</TD>
    </TR>
    <TR>
     <TD>MQTTバージョン</TD>
     <TD>$mqttver_value</TD>
    </TR>
    <TR>
     <TD>TLSバージョン</TD>
     <TD>$tlsver_type</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
Will
<TABLE border="1">
  <TBODY>
    <TR>
     <TD>Will機能</TD>
     <TD>$willon_value</TD>
    </TR>
    <TR>
      <TD>Will topic</TD>
      <TD><INPUT type="text" name="willtopic" size="80" maxlength="128" value="$items{willtopic}" $readonly></TD>
    </TR>
    <TR>
      <TD>Willメッセージ</TD>
      <TD><INPUT type="text" name="willmessage" size="80" maxlength="128" value="$items{willmessage}" $readonly></TD>
    </TR>
    <TR>
     <TD width="200">Will QoS</TD>
     <TD width="230">$willqos_type</TD>
    </TR>
    <TR>
     <TD>Will retain</TD>
     <TD>$willretain_value</TD>
    </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %items = ();
	#設定呼び出し
	%items = &hyper::get_section($section, "", \%item_mqttpubsetup, \%item_def_mqttpubsetup);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_mqttpubsetup;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_mqttpubsetup{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file($section);
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

