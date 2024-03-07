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
  'pppusererror'     => "ȯ���桼��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'ppppasswderror'   => "ȯ���ѥ���ɤ�Ⱦ�ѱѿ���20ʸ������ǻ��ꤷ�Ƥ���������",
 'autherror'   => "ǧ��ͭ��Ǥ�PPP�桼��̾��PPP�ѥ���ɤ϶���ˤ��ʤ��Ǥ���������",
 'waniprerror'      => "WAN¦IP���ɥ쥹�����꤬����������ޤ���",
 'remoteiprerror'   => "��⡼��IP���ɥ쥹�����꤬����������ޤ���",
 'idletimeinterror' => "̵�̿��ƻ���֤������ǻ��ꤷ�Ƥ���������",
 'idletimeerror'    => "̵�̿��ƻ���֤�10����86400�äδ֤ǻ��ꤷ�Ƥ���������",
 'connecttimeinterror' => "�������ǻ��֤������ǻ��ꤷ�Ƥ���������",
 'connecttimeerror'    => "�������ǻ��֤�0�ޤ���60����86400�äδ֤ǻ��ꤷ�Ƥ���������",
 'dnserror_order'   => "DNS������IP�ϥץ饤�ޥ꤫����ꤷ�Ƥ���������",
 'dnserror1'        => "DNS������IP(�ץ饤�ޥ�)�����꤬����������ޤ���",
 'dnserror2'        => "DNS������IP(���������)�����꤬����������ޤ���",
 'dnserror12'       => "DNS������IP(�ץ饤�ޥ�)��DNS������IP(���������)�ϰۤʤ륢�ɥ쥹����ꤷ�Ƥ���������",
 'apnerror'   => "��³��APN��Ⱦ�ѱѿ���31ʸ������ǻ��ꤷ�Ƥ���������",
 'telnumberseterror'   => "��³����ͭ���Ǥ���³���������ֹ����ꤷ�Ƥ���������",
 'telnumbererror'   => "��³���������ֹ��Ⱦ�ѿ���20ʸ������ǻ��ꤷ�Ƥ���������",
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

&hyper::get_args($commandline);			# ���������ؿ�

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
$sms_force = &set_radio3_pr("smsforce", $items{smsforce}, "0", "1", "2",  "�̾���³", "������³", "������Хå��Τ�");
$smsauth_type = &set_radio4_pr("smsauthtype", $items{smsauthtype}, "2", "1", "0", "3",  "CHAP/PAP", "PAP", "CHAP", "ǧ��̵��");

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
		$p = "<INPUT type=\"radio\" name=\"sms\" value=\"0\" checked>̵�� <INPUT type=\"radio\" name=\"sms\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"sms\" value=\"0\" >̵�� <INPUT type=\"radio\" name=\"sms\" value=\"1\" checked>ͭ��";
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
		$p = "<INPUT type=\"radio\" name=\"smsforce\" value=\"0\" checked>̵�� <INPUT type=\"radio\" name=\"smsforce\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"smsforce\" value=\"0\" >̵�� <INPUT type=\"radio\" name=\"smsforce\" value=\"1\" checked>ͭ��";
	}
	return $p;
}

sub input_sreceiveallow {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"sreceiveallow\" value=\"0\" checked>���ꤷ�ʤ�  <INPUT type=\"radio\" name=\"sreceiveallow\" value=\"1\">���ꤹ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"sreceiveallow\" value=\"0\" >���ꤷ�ʤ�  <INPUT type=\"radio\" name=\"sreceiveallow\" value=\"1\" checked>���ꤹ��";
	}
	return $p;
}

sub input_smssend {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"smssend\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"smssend\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"smssend\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"smssend\" value=\"1\" checked>ͭ��";
	}
	return $p;
}

sub input_smspdp {
	my $v = $_[0];
	my $p;

	if ("$v" eq "IP") {
		$p = "<INPUT type=\"radio\" name=\"spdp\" value=\"IP\" checked>IP  <INPUT type=\"radio\" name=\"spdp\" value=\"PPP\">PPP(WCDMA����)";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"spdp\" value=\"IP\" >IP  <INPUT type=\"radio\" name=\"spdp\" value=\"PPP\" checked>PPP(WCDMA����)";
	}
	return $p;
}

sub input_smsdnscheck {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"sdnscheck\" value=\"0\" checked>���ꤷ�ʤ�  <INPUT type=\"radio\" name=\"sdnscheck\" value=\"1\">���ꤹ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"sdnscheck\" value=\"0\" >���ꤷ�ʤ�  <INPUT type=\"radio\" name=\"sdnscheck\" value=\"1\" checked>���ꤹ��";
	}
	return $p;
}

sub input_slcpecho {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"slcpecho\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"slcpecho\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"slcpecho\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"slcpecho\" value=\"1\" checked>ͭ��";
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
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
$err_item
<H2>SMS�忮����</H2>
<FORM name="smssetup" action="./smssetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>

<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">SMS�忮</TD>
     <TD width="200">$sms_sel</TD>
    </TR>

    <TR>
      <TD>��³��APN</TD>
      <TD><INPUT type="text" name="sapn" size="31" maxlength="31" value="$items{sapn}" $readonly></TD>
    </TR>

    <TR>
     <TD width="200">PDP����</TD>
     <TD width="200">$sms_pdp</TD>
    </TR>

    <TR>
     <TD width="200">�İ������ѻ���</TD>
     <TD width="200">$sms_dnscheck</TD>
    </TR>

    <TR>
     <TD width="200">ip����SMS������Хå�</TD>
     <TD width="200">$sms_send</TD>
    </TR>

    <TR>
     <TD width="200">SMS�忮ư��</TD>
     <TD width="330">$sms_force</TD>
    </TR>

  </TBODY>
</TABLE>

<BR>
PPP����
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="200">ǧ������</TD>
      <TD width="330">$smsauth_type</TD>
    </TR>
    <TR>
      <TD>PPP�桼��̾</TD>
      <TD><INPUT type="text" name="spppuser" size="31" maxlength="64" value="$items{spppuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>PPP�ѥ����</TD>
      <TD><INPUT type="password" name="sppppasswd" size="31" maxlength="20" value="$items{sppppasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>WAN¦IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="swanip" size="31" maxlength="15" value="$items{swanip}" $readonly></TD>
    </TR>
    <TR>
      <TD>��⡼��IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="sremoteip" size="31" maxlength="15" value="$items{sremoteip}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(�ץ饤�ޥ�)</TD>
      <TD><INPUT type="text" name="sdhcpdns1" size="31" maxlength="15" value="$items{sdhcpdns1}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(���������)</TD>
      <TD><INPUT type="text" name="sdhcpdns2" size="31" maxlength="15" value="$items{sdhcpdns2}" $readonly></TD>
    </TR>

    <TR>
      <TD>̵�̿��ƻ����</TD>
      <TD><INPUT type="text" name="sidle_time" size="31" maxlength="5" value="$items{sidle_time}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>�������ǻ���</TD>
      <TD><INPUT type="text" name="sconnecttime" size="31" maxlength="5" value="$items{sconnecttime}" $readonly>��</TD>
    </TR>
    <TR>
     <TD width="200">LCP-ECHO�ƻ�</TD>
     <TD width="200">$slcpecho_value</TD>
    </TR>
  </TBODY>
</TABLE>


<BR>
������忮�ꥸ�����ȵ�ǽ
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">��³����</TD>
     <TD width="200">$sreceiveallow_value</TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�1</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber1" value="$items{sallownumber1}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�2</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber2" value="$items{sallownumber2}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�3</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber3" value="$items{sallownumber3}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�4</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber4" value="$items{sallownumber4}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�5</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber5" value="$items{sallownumber5}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�6</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber6" value="$items{sallownumber6}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�7</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber7" value="$items{sallownumber7}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�8</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber8" value="$items{sallownumber8}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�9</TD>
      <TD><INPUT type="text" size="31" maxlength="20" name="sallownumber9" value="$items{sallownumber9}" $readonly></TD>
    </TR>
    <TR>
      <TD>��³���������ֹ�10</TD>
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
	#g����ƤӽФ�
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


