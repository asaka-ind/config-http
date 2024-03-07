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
 'apnerror'   => "��³��(APN)��Ⱦ�ѱѿ���39ʸ������ǻ��ꤷ�Ƥ���������",
 'telnumberseterror'   => "��³�����ͭ���Ǥ���³���������ֹ����ꤷ�Ƥ���������",
 'telnumbererror'   => "��³���������ֹ��Ⱦ�ѿ���20ʸ������ǻ��ꤷ�Ƥ���������",
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

&hyper::get_args($commandline);			# ���������ؿ�

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
#$connect_value = &set_radio3_pr("connect", $items{connect}, "0", "1", "2",  "�����³", "���٥����³", "ȯ�����ʤ�(SMS�Τߡ�");
$auth_type = &set_radio4_pr("authtype", $items{authtype}, "3", "1", "2", "0",  "CHAP/PAP", "PAP", "CHAP", "ǧ��̵��");

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
		$p = "<INPUT type=\"radio\" name=\"keeppacket\" value=\"0\" checked>�ݻ��ѥ��å�ͭ�� <INPUT type=\"radio\" name=\"keeppacket\" value=\"1\">�ݻ��ѥ��å�̵��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"keeppacket\" value=\"0\" >�ݻ��ѥ��å�ͭ�� <INPUT type=\"radio\" name=\"keeppacket\" value=\"1\" checked>�ݻ��ѥ��å�̵��";
	}
	return $p;
}

sub input_dialicmp {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dialicmp\" value=\"0\" checked>���Ĥ��ʤ� <INPUT type=\"radio\" name=\"dialicmp\" value=\"1\">���Ĥ���";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dialicmp\" value=\"0\" >���Ĥ��ʤ� <INPUT type=\"radio\" name=\"dialicmp\" value=\"1\" checked>���Ĥ���";
	}
	return $p;
}

sub input_dialdns {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dialdns\" value=\"0\" checked>���Ĥ��ʤ� <INPUT type=\"radio\" name=\"dialdns\" value=\"1\">���Ĥ���";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dialdns\" value=\"0\" >���Ĥ��ʤ� <INPUT type=\"radio\" name=\"dialdns\" value=\"1\" checked>���Ĥ���";
	}
	return $p;
}

sub input_dnscheck {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dnscheck\" value=\"0\" checked>���ꤷ�ʤ� <INPUT type=\"radio\" name=\"dnscheck\" value=\"1\">���ꤹ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dnscheck\" value=\"0\" >���ꤷ�ʤ� <INPUT type=\"radio\" name=\"dnscheck\" value=\"1\" checked>���ꤹ��";
	}
	return $p;
}

sub input_pdp {
	my $v = $_[0];
	my $p;

	if ("$v" eq "IP") {
		$p = "<INPUT type=\"radio\" name=\"pdp\" value=\"IP\" checked>IP  <INPUT type=\"radio\" name=\"pdp\" value=\"PPP\">PPP(WCDMA����)";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"pdp\" value=\"IP\" >IP  <INPUT type=\"radio\" name=\"pdp\" value=\"PPP\" checked>PPP(WCDMA����)";
	}
	return $p;
}


sub input_connect {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"connect\" value=\"0\" checked>�����³  <INPUT type=\"radio\" name=\"connect\" value=\"1\">���٥����³";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"connect\" value=\"0\" >�����³  <INPUT type=\"radio\" name=\"connect\" value=\"1\" checked>���٥����³";
	}
	return $p;
}

sub input_wancheck {
        my $v = $_[0];
        my $p;

        if ("$v" eq "0") {
                $p = "<INPUT type=\"radio\" name=\"wancheck\" value=\"0\" checked>ͭ��  <INPUT type=\"radio\" name=\"wancheck\" value=\"1\">̵��";
        }
        else {
                $p = "<INPUT type=\"radio\" name=\"wancheck\" value=\"0\" >ͭ��  <INPUT type=\"radio\" name=\"wancheck\" value=\"1\" checked>̵��";
        }
        return $p;
}

sub input_lcpecho {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"lcpecho\" value=\"0\" checked>̵��  <INPUT type=\"radio\" name=\"lcpecho\" value=\"1\">ͭ��";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"lcpecho\" value=\"0\" >̵��  <INPUT type=\"radio\" name=\"lcpecho\" value=\"1\" checked>ͭ��";
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
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
$err_item
<H2>WAN����</H2>
<FORM name="wansetup" action="./wansetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>

<BR>
PPP����
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">ǧ������</TD>
     <TD width="330">$auth_type</TD>
    </TR>
    <TR>
      <TD>PPP�桼��̾</TD>
      <TD><INPUT type="text" name="pppuser" size="31" maxlength="64" value="$items{pppuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>PPP�ѥ����</TD>
      <TD><INPUT type="password" name="ppppasswd" size="31" maxlength="20" value="$items{ppppasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>WAN¦IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="wanip" size="31" maxlength="15" value="$items{wanip}" $readonly></TD>
    </TR>
    <TR>
      <TD>��⡼��IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="remoteip" size="31" maxlength="15" value="$items{remoteip}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(�ץ饤�ޥ�)</TD>
      <TD><INPUT type="text" name="dhcpdns1" size="31" maxlength="15" value="$items{dhcpdns1}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(���������)</TD>
      <TD><INPUT type="text" name="dhcpdns2" size="31" maxlength="15" value="$items{dhcpdns2}" $readonly></TD>
    </TR>

    <TR>
      <TD>̵�̿��ƻ����</TD>
      <TD><INPUT type="text" name="idle_time" size="31" maxlength="5" value="$items{idle_time}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>�������ǻ���</TD>
      <TD><INPUT type="text" name="connecttime" size="31" maxlength="5" value="$items{connecttime}" $readonly>��</TD>
    </TR>
    <TR>
     <TD width="200">LCP-ECHO�ƻ�</TD>
     <TD width="200">$lcpecho_value</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
ȯ������
<TABLE border="1">
  <TBODY>

<!--
    <TR>
     <TD width="200">����ꥢ</TD>
     <TD width="300">$optcarrierid</TD>
    </TR>
-->

    <TR>
     <TD width="200">��³����</TD>
     <TD width="380">$connect_value</TD>
    </TR>

    <TR>
     <TD width="200">�����³</TD>
     <TD width="300">$keep_packet</TD>
    </TR>

    <TR>
      <TD>��³��APN</TD>
      <TD><INPUT type="text" name="apn" size="39" maxlength="39" value="$items{apn}" $readonly></TD>
    </TR>

<!--
    <TR>
     <TD>PDP����</TD>
     <TD>$pdp_value</TD>
    </TR>
-->

    <TR>
     <TD>ICMP�ץ�ȥ���ˤ��ȯ��</TD>
     <TD>$dialicmp_value</TD>
    </TR>
    <TR>
     <TD>DNS(UDP:53)�ˤ��ȯ��</TD>
     <TD>$dialdns_value</TD>
    </TR>
    <TR>
     <TD>�İ������ѻ���</TD>
     <TD>$dnscheck_value</TD>
    </TR>
    <TR>
     <TD width="200">��³�ƻ�</TD>
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
	#g����ƤӽФ�
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

