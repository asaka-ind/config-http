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
 'pubusererror'     => "ǧ�ڥ桼��̾��Ⱦ�ѱѿ���128ʸ������ǻ��ꤷ�Ƥ���������",
 'pubpasswderror'   => "ǧ�ڥѥ���ɤ�Ⱦ�ѱѿ���256ʸ������ǻ��ꤷ�Ƥ���������",
 'iperror'        => "��³������꤬����������ޤ���",
 'topicerror'   => "TOPIC��Ⱦ�ѱѿ���128ʸ������ǻ��ꤷ�Ƥ���������",
 'pubautherror'   => "ǧ�ڥ桼��̾��ǧ�ڥѥ���ɤ���ꤷ�Ƥ���������",
 'pubiderror'     => "���饤�����ID��Ⱦ�ѱѿ���128ʸ������ǻ��ꤷ�Ƥ���������",
 'willmeserror'     => "Will��å�������Ⱦ�ѱѿ���128ʸ������ǻ��ꤷ�Ƥ���������",
 'portinterror'   => "�ݡ����ֹ�������ǻ��ꤷ�Ƥ���������",
 'porterror'      => "�ݡ����ֹ��1����65535���ϰϤǻ��ꤷ�Ƥ���������",
 'keepaliveinterror'   => "�����ץ��饤�֤������ǻ��ꤷ�Ƥ���������",
 'keepaliveerror'      => "�����ץ��饤�֤�2����65535���ϰϤǻ��ꤷ�Ƥ���������",
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

&hyper::get_args($commandline);			# ���������ؿ�

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
		$p = "<INPUT type=\"radio\" name=\"pubon\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"pubon\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"pubon\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"pubon\" value=\"1\" checked>ͭ��";
	}
	return $p;
}

sub input_willon {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"willon\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"willon\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"willon\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"willon\" value=\"1\" checked>ͭ��";
	}
	return $p;
}

sub input_authon {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"authon\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"authon\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"authon\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"authon\" value=\"1\" checked>ͭ��";
	}
	return $p;
}

sub input_protocol {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"protocol\" value=\"0\" checked>MQTTS(�Ź沽)  <INPUT type=\"radio\" name=\"protocol\" value=\"1\">MQTT";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"protocol\" value=\"0\" >MQTTS(�Ź沽)  <INPUT type=\"radio\" name=\"protocol\" value=\"1\" checked>MQTT";
	}
	return $p;
}

sub input_clientcrt {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"clientcrt\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"clientcrt\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"clientcrt\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"clientcrt\" value=\"1\" checked>ͭ��";
	}
	return $p;
}

sub input_retain {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"retain\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"retain\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"retain\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"retain\" value=\"1\" checked>ͭ��";
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
		$p = "<INPUT type=\"radio\" name=\"willretain\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"willretain\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"willretain\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"willretain\" value=\"1\" checked>ͭ��";
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
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
$err_item
<H2>MQTT�ѥ֥�å��㡼����</H2>
<FORM name="mqttpubsetup" action="./mqttpubsetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>


<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD>�ѥ֥�å��㡼��ǽ</TD>
     <TD>$pubon_value</TD>
    </TR>
    <TR>
     <TD>�ץ�ȥ���</TD>
     <TD>$protocol_value</TD>
    </TR>
    <TR>
      <TD>�ݡ����ֹ�</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="mqttport" value="$items{mqttport}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³��֥�����</TD>
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
     <TD>�桼��̾/�ѥ����ǧ��</TD>
     <TD>$authon_value</TD>
    </TR>
    <TR>
      <TD>���桼��̾</TD>
      <TD><INPUT type="text" name="pubuser" size="80" maxlength="128" value="$items{pubuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>���ѥ����</TD>
      <TD><INPUT type="password" name="pubpasswd" size="80" maxlength="256" value="$items{pubpasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>���饤�����ID</TD>
      <TD><INPUT type="text" name="pubid" size="80" maxlength="128" value="$items{pubid}" $readonly></TD>
    </TR>
    <TR>
      <TD>�����ץ��饤��(MQTT-PING)</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="keepalive" value="$items{keepalive}" $readonly>��</TD>
    </TR>
    <TR>
     <TD>Retain</TD>
     <TD>$retain_value</TD>
    </TR>
    <TR>
     <TD>���饤����Ⱦ�����</TD>
     <TD>$clientcrt_value</TD>
    </TR>
    <TR>
     <TD>MQTT�С������</TD>
     <TD>$mqttver_value</TD>
    </TR>
    <TR>
     <TD>TLS�С������</TD>
     <TD>$tlsver_type</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
Will
<TABLE border="1">
  <TBODY>
    <TR>
     <TD>Will��ǽ</TD>
     <TD>$willon_value</TD>
    </TR>
    <TR>
      <TD>Will topic</TD>
      <TD><INPUT type="text" name="willtopic" size="80" maxlength="128" value="$items{willtopic}" $readonly></TD>
    </TR>
    <TR>
      <TD>Will��å�����</TD>
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
	#����ƤӽФ�
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

