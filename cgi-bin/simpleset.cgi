#!/usr/bin/perl -w

require "hyper.pl";
require "wan.pl";

# general
%item_general = (
 'hostname' => "hostname",
);

%item_def_general = (
 'hostname' => "",
);

#machine
%item_machine = (
 'name'    => "name",
 'version' => "version",
 'kversion' => "kversion",
);

%item_def_machine = (
 'name'    => "",
 'version' => "",
 'kversion' => "",
);

#serial
%item_serial = (
 'serial' => "serial",
 'macadr1' => "macadr1",
);
%item_def_serial = (
 'serial' => "",
 'macadr1' => "",
);

#network
%item_network = (
 'ipadr1'     => "ipadr1",
 'subnetadr1' => "subnetadr1",
);

%item_def_network = (
 'ipadr1'     => "192.168.1.100",
 'subnetadr1' => "255.255.255.0",
);

#dhcp
%item_dhcpsetup = (
 'dhcpserver'   => "dhcpserver",
 'dhcpstart'    => "dhcpstart",
 'dhcpend'      => "dhcpend",
 'dhcpsubnet'   => "dhcpsubnet",
 'dhcpgateads'  => "dhcpgateads",
 'dhcptime'     => "dhcptime",
);

%item_def_dhcpsetup = (
 'dhcpserver'   => "0",
 'dhcpstart'    => "192.168.1.2",
 'dhcpend'      => "192.168.1.2",
 'dhcpsubnet'   => "255.255.255.0",
 'dhcpgateads'  => "192.168.1.1",
 'dhcptime'     => "600",
);

#etc
%item_etcsetup = (
 'icmp'      => "icmp",
 'virtserve' => "virtserve",
 'virtip'    => "virtip",
);

%item_def_etcsetup = (
 'icmp'      => "0",
 'virtserve' => "0",
 'virtip'    => "",
);

#ddns
%item_ddnssetup = (
 'ddnsuser'         => "ddnsuser",
 'ddnspasswd'       => "ddnspasswd",
 'ddnsserver'	    => "ddnsserver",
 'ddnsname'	    => "ddnsname",
 'ddns_onoff'	    => "ddns_onoff",
);

%item_def_ddnssetup = (
 'ddnsuser'         => "",
 'ddnspasswd'       => "",
 'ddnsserver'	    => "1",
 'ddnsname'	    => "",
 'ddns_onoff'	    => "0",
);

# wansetup items
%item_wansetup = ();
%item_def_wansetup = ();

&wan::make_list(\%item_wansetup, \%item_def_wansetup);


%item_list = (%item_general, %item_machine, %item_serial, %item_network, %item_dhcpsetup,  %item_etcsetup, %item_ddnssetup, %item_wansetup);

#%item_def = (%item_def_general, %item_def_machine, %item_def_serial, %item_def_network, %item_def_dhcpsetup, %item_def_etcsetup, %item_def_ddnssetup,  %item_def_wansetup);



%error_list = (
 'hostnameerr'  => "�ۥ���̾�����꤬����������ޤ���",

 'lanipadrerror'     => "LAN��IP���ɥ쥹�����꤬����������ޤ���",
 'lansubnetadrerror' => "LAN�Υ��֥ͥåȥޥ��������꤬����������ޤ���",

 'dhcpstartadrerror'    => "���۳���IP���ɥ쥹�����꤬����������ޤ���",
 'dhcpendadrerror'      => "���۽�λIP���ɥ쥹�����꤬����������ޤ���",
 'dhcpstartendadrerror' => "���۽�λIP���ɥ쥹�����۳��ϥ��ɥ쥹����礭�����ɥ쥹����ꤷ�Ƥ���������",
 'dhcpsubmaskerror'     => "���ۥ��֥ͥåȤ����꤬����������ޤ���",
 'dhcpgateadserror'     => "���ۥǥե���ȥ����ȥ����������꤬����������ޤ���",
 'dhcptimeinterror'     => "�꡼�����֤������ǻ��ꤷ�Ƥ���������",
 'dhcptimeerror'        => "�꡼�����֤�1����1440ʬ���ϰϤǻ��ꤷ�Ƥ���������",

 'vsipadrerror'     => "�С�����륵����������IP���ɥ쥹�����꤬����������ޤ���",

 'ddnsnameerror'     => "�����ʥߥå�DNS�ɥᥤ��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'ddnsusererror'     => "�����ʥߥå�DNS�桼��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'ddnspasswderror'   => "�����ʥߥå�DNS�ѥ���ɤ�Ⱦ�ѱѿ���20ʸ������ǻ��ꤷ�Ƥ���������",

 'pppusererror'     => "ȯ���桼��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'ppppasswderror'   => "ȯ���ѥ���ɤ�Ⱦ�ѱѿ���20ʸ������ǻ��ꤷ�Ƥ���������",
 'waniprerror'      => "ȯ�������WAN¦IP���ɥ쥹�����꤬����������ޤ���",
 'remoteiprerror'   => "ȯ������Υ�⡼��IP���ɥ쥹�����꤬����������ޤ���",
 'idletimeinterror' => "̵�̿��ƻ���֤������ǻ��ꤷ�Ƥ���������",
 'idletimeerror'    => "̵�̿��ƻ���֤�0�ޤ���60����86400�äδ֤ǻ��ꤷ�Ƥ���������",
 'connecttimeinterror' => "�������ǻ��֤������ǻ��ꤷ�Ƥ���������",
 'connecttimeerror'    => "�������ǻ��֤�0�ޤ���60����86400�äδ֤ǻ��ꤷ�Ƥ���������",
 'dnserror_order'   => "DNS������IP�ϥץ饤�ޥ꤫����ꤷ�Ƥ���������",
 'dnserror1'        => "DNS������IP(�ץ饤�ޥ�)�����꤬����������ޤ���",
 'dnserror2'        => "DNS������IP(���������)�����꤬����������ޤ���",
 'dnserror12'       => "DNS������IP(�ץ饤�ޥ�)��DNS������IP(���������)�ϰۤʤ륢�ɥ쥹����ꤷ�Ƥ���������",
 'rpppusererror'     => "�忮�桼��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'rppppasswderror'   => "�忮�ѥ���ɤ�Ⱦ�ѱѿ���20ʸ������ǻ��ꤷ�Ƥ���������",
 'rwaniprerror'      => "�忮�����WAN¦IP���ɥ쥹�����꤬����������ޤ���",
 'rremoteiprerror'   => "�忮����Υ�⡼��IP���ɥ쥹�����꤬����������ޤ���",
 'ruserpasswderror'   => "ȯ�����忮�ǥ桼��̾��Ʊ���ǥѥ���ɤ���äƤ��ޤ����ѥ���ɤ�Ʊ�����뤫���㤦�桼��̾�ˤ��Ƥ���������",
 'connectmodeerror'   => "�����³�Ǥϡ�������³������ȯ���Τߤ�����ˤ��Ƥ���������",
 'disconnecttimeerror' => "�������ǻ�������������ͤ�������������ޤ���",
);

$commandline = "";
%items = ();
$setting = "";
$settm = "";
$err_item ="";
$dialicmp_value ="";
$dialdns_value ="";
$pdp_value ="";
$pppauth_value ="";
$connect_value ="";
$receive_set = "";
$SetRestart = "";
$restart_time = 0;
$restitle = "";
$discont_nums = 4;

$readonly ="";
$disabled ="";
if (!&hyper::get_logincheck()) {
	$disabled = "disabled";
	$readonly = "readonly";
}

&hyper::get_args($commandline);			# ���������ؿ�

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
	$settm = &hyper::get_param("btnSettm", $commandline);
	$dtime = &hyper::get_param("dtime", $commandline);
	$SetRestart = &hyper::get_param("btnSetrestart", $commandline);
}


#���λ�������
if ($settm ne "") {
	if (defined($dtime)) {
		my $dcommand = "/bin/date \'$dtime\'";
		my $rev = system("$dcommand &");
		sleep(1);
		system("/sbin/hwclock -w");
	}
}

%items = &get_item();


if ($setting ne "" ) {
	for(my $i = 1; $i <= $discont_nums; $i++){
		$items{"discontch$i"} = "0";
	}

	my @Keys = keys %item_list;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);
	}
}

#�����Ƶ�ư�¹�
elsif($SetRestart ne ""){
	for(my $i = 1; $i <= $discont_nums; $i++){
		$items{"discontch$i"} = "0";
	}

	my @Keys = keys %item_list;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);

		my @Values = values %hyper::cfg_name;

		foreach my $v (@Values) {
			my $file = &hyper::get_temp_file($v);
			if (-e $file) {
				my $cpfile = &hyper::get_modify_file($v);
				my @Buff = &hyper::readfile($file);
				&hyper::writefile($cpfile, @Buff);
			}
		}

	#�ѹ��ե饰��Ω�Ƥ�
		my $flag = &hyper::get_flag_file($hyper::flag_name{'modify'});
		my @s = ("1");
		&hyper::writefile($flag, @s);
	#�Ƶ�ư�ե饰��Ω�Ƥ�
		$flag = &hyper::get_flag_file($hyper::flag_name{'reboot'});
		&hyper::writefile($flag, @s);
		$restart_time = 60;
		$restitle = "������¸�ȺƵ�ư";
		&pr_restart();
		exit;
	}
}

$items{hostname} = uc $items{hostname};
my $dcommand = "date \'+%Y/%m/%d %k:%M:%S\'";
my $hltime = `$dcommand`;

$dhcp_value = set_radio_pr("dhcpserver", $items{dhcpserver}, "0", "1", "OFF", "ON");

$icmp_value = set_radio_pr("icmp", $items{icmp}, "0", "1", "��������", "�롼������");

$virtserve_value = set_radio_pr("virtserve", $items{virtserve}, "0", "1", "̵��", "ͭ��");

$ddns_onoff = set_radio_pr("ddns_onoff", $items{ddns_onoff}, "0", "1",  "OFF", "ON");

$dialicmp_value = set_radio_pr("dialicmp", $items{dialicmp}, "0", "1", "���Ĥ��ʤ�", "���Ĥ���");

$dialdns_value = set_radio_pr("dialdns", $items{dialdns}, "0", "1", "���Ĥ��ʤ�", "���Ĥ���");

$pdp_value = set_radio_pr("pdp", $items{pdp}, "ppp", "ip", "PPP", "IP");

$pppauth_value = set_radio_pr("pppauth", $items{pppauth}, "0", "1", "CHAP/PAP", "PAP�Τ�");

$connect_value = set_radio_pr("connect", $items{connect}, "0", "1", "�����³", "���٥����³");

sub chk_item {
	my %items = @_;

	#general
	my$hostname = uc $items{hostname};
	my $d =&hyper::checkhoststring($hostname);
	if ($d eq "") {
		return "hostnameerr";
	}

	#lan
	if (&hyper::get_ipaddress($items{ipadr1}) eq "") {
		return "lanipadrerror";
	}
	if (&hyper::get_submask($items{subnetadr1}) eq "") {
		return "lansubnetadrerror";
	}

	#dhcp
	my $use = $items{'dhcpserver'};

	if (($use eq "1") ||
		(length $items{dhcpstart}) ||
		(length $items{dhcpend})   ||
		(length $items{dhcpsubnet}) ||
		(length $items{dhcpgateads})) {
		if (&hyper::get_ipaddress($items{dhcpstart}) eq "") {
			return "dhcpstartadrerror";
		}
		if (&hyper::get_ipaddress($items{dhcpend}) eq "") {
			return "dhcpendadrerror";
		}
		my @start = split(/\./, $items{dhcpstart});
		my @end   = split(/\./, $items{dhcpend});
		my $s = ($start[0]*(2**24))+($start[1]*(2**16))+($start[2]*(2**8))+$start[3];
		my $e = ($end[0]*(2**24))+($end[1]*(2**16))+($end[2]*(2**8))+$end[3];
		if ($e < $s) {
			return "dhcpstartendadrerror";
		}
		if (&hyper::get_submask($items{dhcpsubnet}) eq "") {
			return "dhcpsubmaskerror";
		}

		if (&hyper::get_ipaddress($items{dhcpgateads}) eq "") {
			return "dhcpgateadserror";
		}
	}

	if (&hyper::checknumstring($items{dhcptime}) == 0) {
		return "dhcptimeinterror";
	}

	if (($items{dhcptime} < 1) || ($items{dhcptime} > 1440)) {
		return "dhcptimeerror";
	}

	#etc
	if (($items{virtserve} eq "1") || ($items{virtip} ne "")) {
		if (&hyper::get_ipaddress($items{virtip}) eq "") {
			return "vsipadrerror";
		}
	}

	#ddns
	if (&chk_graph($items{ddnsname}, 64) eq "" ) {
		return "ddnsnameerror";
	}

	if (&chk_graph($items{ddnsuser}, 64) eq "" ) {
		return "ddnsusererror";
	}

	if (&chk_graph($items{ddnspasswd}, 20) eq "" ) {
		return "ddnspasswderror";
	}

	#wan
	if (($items{connect} eq "0") and ($items{dialtype} ne "2")) {
		return "connectmodeerror";
	}

	if (&chk_graph($items{pppuser}, 64) eq "" ) {
		return "pppusererror";
	}

	if (&chk_graph($items{ppppasswd}, 20) eq "" ) {
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

	if ($items{idle_time} != 0) {
		if (($items{idle_time} < 60) || ($items{idle_time} > 86400)) {
			return "idletimeerror";
		}
	}
	if (&hyper::checknumstring($items{connecttime}) == 0) {
		return "connecttimeinterror";
	}

	if ($items{connecttime} != 0) {
		if (($items{connecttime} < 60) || ($items{connecttime} > 86400)) {
			return "connecttimeerror";
		}
	}

	for(my $i = 1; $i <= $discont_nums; $i++){
		if($items{"discontch$i"} eq "0"){
			if((!length $items{"disconth$i"}) and (!length $items{"discontm$i"})){
				next;
			}
		}
		if (&hyper::checknumstring($items{"disconth$i"}) == 0) {
 			return "disconnecttimeerror";
		}
		if (($items{"disconth$i"} < 0) || ($items{"disconth$i"} > 23)) {
			return "disconnecttimeerror";
		}
		if (&hyper::checknumstring($items{"discontm$i"}) == 0) {
 			return "disconnecttimeerror";
		}
		if (($items{"discontm$i"} < 0) || ($items{"discontm$i"} > 59)) {
			return "disconnecttimeerror";
		}
	}

	if (&chk_graph($items{rpppuser}, 64) eq "" ) {
		return "rpppusererror";
	}

	if (&chk_graph($items{rppppasswd}, 20) eq "" ) {
		return "rppppasswderror";
	}

	if ($items{rwanip} ne "") {
		if (&hyper::get_ipaddress($items{rwanip}) eq "") {
			return "rwaniprerror";
		}
	}
	if ($items{rremoteip} ne "") {
		if (&hyper::get_ipaddress($items{rremoteip}) eq "") {
			return "rremoteiprerror";
		}
	}

	if ($items{pppuser} eq $items{rpppuser}) {
		if ($items{ppppasswd}  ne $items{rppppasswd}) {
			return "ruserpasswderror";
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

sub set_radio_pr{
	my ($name,$v,$value0,$value1,$va_pr0,$va_pr1) = @_;
	my $p = "";
	my $checked0 = "";
	my $checked1 = "";

	if("$v" eq "$value0"){
		$checked0 = "checked";
	}else{
		$checked1 = "checked";
	}
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0>$va_pr0 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1>$va_pr1";
	
	return $p;
}

sub input_receive {
	my $p = "";
	my $num = 0;

	$p = $p."<TR><TD align=\"left\"  colspan=\"2\">��³��(APN/�����ֹ�)</TD></TR>";
	for(my $i = 0; $i < 10; $i++){
		$num = $i + 1;
		$p = $p."<TR><TD align=\"right\">$num</TD>";
		$p = $p."<TD><INPUT type=\"text\" size=\"31\" maxlength=\"31\" name=\"callingid$i\" value=\"$items{\"callingid$i\"}\"></TD></TR>";
	}
	return $p;
}

sub input_disconntime {
	my $p = "";
	my $num = 0;
	my $check = "";

	$p = $p."<TR><TD align=\"left\"  colspan=\"2\">�������ǻ�������</TD></TR>";
	for(my $i = 1; $i <= $discont_nums; $i++){
		$num = $i;
		if ($items{"discontch$i"} eq "1" ){
			$check = "checked";
		}else{
			$check = "";
		}
		$p = $p."<TR><TD align=\"right\"><INPUT type=\"checkbox\" name=\"discontch$num\" value=\"1\" $check $disabled>����$num</TD>";
		$p = $p."<TD align=\"center\"><INPUT type=\"text\" size=\"3\" maxlength=\"2\" name=\"disconth$i\" value=\"$items{\"disconth$i\"}\" >����";
		$p = $p."<INPUT type=\"text\" size=\"3\" maxlength=\"2\" name=\"discontm$i\" value=\"$items{\"discontm$i\"}\" >ʬ</TD></TR>";
	}
	return $p;
}

$receive_set = &input_receive();

my $optcidsel = &opt_cidsel($items{"cid"});
my $opttypesel = &opt_typesel($items{"dialtype"});
my $rpacketsel = &rec_packetsel($items{"rpacket"});
my $rdialsel = &rec_dialsel($items{"rdial"});
my $disconntime_value = &input_disconntime();

$optddnssel = &opt_ddnssel($items{"ddnsserver"});

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<SCRIPT language="JavaScript">
var chpass = false;
function time() {
var now=new Date();
year=now.getYear();
if(year<2000){year=year+1900;}
month=now.getMonth()+1;
date=now.getDate();
day=new Array("��","��","��","��","��","��","��");
day=day[now.getDay()];
hour=now.getHours();
minute=now.getMinutes();
second=now.getSeconds();
if(month<="9"){month="0"+month;};
if(date<="9"){date="0"+date;};
if(hour<="9"){hour="0"+hour;};
if(minute<="9"){minute="0"+minute;};
if(second<="9"){second="0"+second;};
document.form1.watch.value=year+"/"+month+"/"+date+" "+hour+":"+minute+":"+second;
document.form1.dtime.value=year+"."+month+"."+date+"-"+hour+":"+minute+":"+second;
setTimeout('time()',1000);
}
</SCRIPT>
<TITLE>�ʰ�����</TITLE>
<LINK href="hpbsite.css" rel="stylesheet" type="text/css">
<style type="text/css">
<!--
BODY, TH, TD {font-size: x-small }
TABLE { table-layout: fixed}
-->
</style>
</HEAD>
<BODY bgcolor="#cccccc"  onload="time();">
$err_item
<H2>�ʰ�����</H2>
<FORM name="form1" action="./simpleset.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����" $disabled> 
<INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>
<A href="../html/subindex.html" target="_top">�ܺ������</A>
<INPUT type="submit" name="btnSetrestart" value="������¸�ȺƵ�ư�¹�" $disabled> 
<TABLE border="0">
  <TBODY style="vertical-align: top">
    <TR>  <TD width="420">
�����ξ���
<TABLE border="1" cellpadding="3">
  <TBODY style="vertical-align: middle">
    <TR>
      <TD width="200">���η���</TD>
      <TD width="200">$items{'name'}</TD>
    </TR>
    <TR>
      <TD>��¤�ֹ�</TD>
      <TD>$items{serial}</TD>
    </TR>
    <TR>
      <TD>�С������</TD>
      <TD>$items{'version'} \($items{'kversion'} \)</TD>
    </TR>
    <TR>
      <TD>�ۥ���̾</TD>
      <TD><INPUT size="31" type="text" maxlength="31" name="hostname" value="$items{hostname}" $readonly></TD>
    </TR>
    <TR>
      <TD>���λ���</TD>
      <TD>$hltime</TD>
    </TR> 
   <TR>
      <TD>���߻���(PC�λ���)</TD>
      <TD><INPUT name="watch" size="31" readonly>
          <INPUT type="submit" name="btnSettm" value="��������" $disabled>
          <INPUT type="hidden" name="dtime" value="">
      </TD>
    </TR>
  </TBODY>
</TABLE>
	     </TD>
		<TD width="420">
��DHCP����
<TABLE border="1" cellpadding="3">
  <TBODY style="vertical-align: middle">
   <TR>
     <TD width="200">DHCP������</TD>
     <TD width="200">$dhcp_value</TD>
   </TR>
   <TR>
     <TD>���۳���IP���ɥ쥹</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpstart" value="$items{dhcpstart}"></TD>
   </TR>
   <TR>
     <TD>���۽�λIP���ɥ쥹</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpend" value="$items{dhcpend}"></TD>
   </TR>
   <TR>
     <TD>���ۥ��֥ͥåȥޥ���</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpsubnet" value="$items{dhcpsubnet}"></TD>
   </TR>
   <TR>
     <TD>���ۥǥե���ȥ����ȥ�����</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpgateads" value="$items{dhcpgateads}"></TD>
   </TR>
   <TR>
     <TD>�꡼������</TD>
     <TD><INPUT size="20" type="text" maxlength="4" name="dhcptime" value="$items{dhcptime}">ʬ</TD>
   </TR>
  </TBODY>
</TABLE>
		</TD>
	</TR>
    <TR>  <TD>
��LAN����
<TABLE border="1" cellpadding="3">
  <TBODY style="vertical-align: middle">
    <TR>
      <TD width="200">MAC���ɥ쥹</TD>
      <TD width="200">$items{macadr1}</TD>
    </TR>
    <TR>
      <TD>IP���ɥ쥹</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="ipadr1" value="$items{ipadr1}" $readonly></TD>
    </TR>
    <TR>
      <TD>���֥ͥåȥޥ���</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="subnetadr1" value="$items{subnetadr1}" $readonly></TD>
    </TR>
  </TBODY>
</TABLE>
     </TD>
		<TD>
������¾����
<TABLE border="1" cellpadding="3">
  <TBODY style="vertical-align: middle">
    <TR>
      <TD width="200">ICMP����</TD>
        <TD width="200">$icmp_value</TD>
    </TR>
    <TR>
      <TD>�С�����륵���е�ǽ</TD>
        <TD>$virtserve_value</TD>
    </TR>
    <TR>
      <TD>�С�����륵����������IP���ɥ쥹</TD>
      <TD><INPUT size="20" type="text" maxlength="15" name="virtip" value="$items{virtip}" $readonly></TD>
    </TR>
  </TBODY>
</TABLE>
		</TD>
	</TR>
	<TR><TD>
����³����
<TABLE border="1">
  <TBODY style="vertical-align: middle">
    <TR>
      <TD width="200">������³����</TD>
      <TD width="200">$opttypesel</TD>
    </TR>
    <TR>
     <TD>��³����</TD>
     <TD>$connect_value</TD>
    </TR>
    <TR>
      <TD>̵�̿��ƻ����</TD>
      <TD><INPUT type="text" name="idle_time" size="20" maxlength="5" value="$items{idle_time}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>�������ǻ���</TD>
      <TD><INPUT type="text" name="connecttime" size="20" maxlength="5" value="$items{connecttime}" $readonly>��</TD>
    </TR>
	$disconntime_value
  </TBODY>
</TABLE>
	</TD>
	<TD>
�������ʥߥå�DNS
<TABLE border="1">
  <TBODY style="vertical-align: middle">
    <TR>
     <TD width="200">�����ʥߥå�DNS</TD>
     <TD width="200">$ddns_onoff</TD>
    </TR>
   
    <TR>
      <TD>�����ʥߥå�DNS������</TD>
      <TD width="150">$optddnssel</TD>
    </TR>

    <TR>
      <TD>�ɥᥤ��̾</TD>
      <TD><INPUT type="text" name="ddnsname" size="31" maxlength="31" value="$items{ddnsname}" $readonly></TD>
    </TR>

    <TR>
      <TD>�桼��̾</TD>
      <TD><INPUT type="text" name="ddnsuser" size="31" maxlength="64" value="$items{ddnsuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>�ѥ����</TD>
      <TD><INPUT type="password" name="ddnspasswd" size="20" maxlength="20" value="$items{ddnspasswd}" $readonly></TD>
    </TR>
  </TBODY>
</TABLE>
	</TD></TR>
	<TR><TD>
��ȯ������
<TABLE border="1">
  <TBODY style="vertical-align: middle">
    <TR>
      <TD width="200">CID�ֹ�</TD>
      <TD width="200">$optcidsel</TD>
    </TR>
    <TR>
      <TD>��³��(APN/�����ֹ�)</TD>
      <TD><INPUT type="text" name="apn" size="31" maxlength="31" value="$items{apn}" $readonly></TD>
    </TR>
    <TR>
     <TD>PDP����</TD>
     <TD>$pdp_value</TD>
    </TR>
    <TR>
     <TD>PPPǧ�ڥ⡼��</TD>
     <TD>$pppauth_value</TD>
    </TR>
    <TR>
      <TD>ȯ��PPP�桼��̾</TD>
      <TD><INPUT type="text" name="pppuser" size="31" maxlength="64" value="$items{pppuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>ȯ��PPP�ѥ����</TD>
      <TD><INPUT type="password" name="ppppasswd" size="20" maxlength="20" value="$items{ppppasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(�ץ饤�ޥ�)</TD>
      <TD><INPUT type="text" name="dhcpdns1" size="20" maxlength="15" value="$items{dhcpdns1}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(���������)</TD>
      <TD><INPUT type="text" name="dhcpdns2" size="20" maxlength="15" value="$items{dhcpdns2}" $readonly></TD>
    </TR>
    <TR>
      <TD>WAN¦IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="wanip" size="20" maxlength="15" value="$items{wanip}" $readonly></TD>
    </TR>
    <TR>
      <TD>��⡼��IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="remoteip" size="20" maxlength="15" value="$items{remoteip}" $readonly></TD>
    </TR>
    <TR>
     <TD>ICMP�ץ�ȥ���ˤ��ȯ��</TD>
     <TD>$dialicmp_value</TD>
    </TR>
    <TR>
     <TD>DNS(UDP:53)�ˤ��ȯ��</TD>
     <TD>$dialdns_value</TD>
    </TR>
  </TBODY>
</TABLE>
	</TD>
	<TD>
���忮����
<TABLE border="1">
  <TBODY style="vertical-align: middle">
    <TR>
	  <TD width="200">�忮PPP�桼��̾</TD>
      <TD width="200"><INPUT type="text" name="rpppuser" size="31" maxlength="64" value="$items{rpppuser}" $readonly></TD>
    </TR>
    <TR>
	  <TD>�忮PPP�ѥ����</TD>
      <TD><INPUT type="password" name="rppppasswd" size="20" maxlength="20" value="$items{rppppasswd}" $readonly></TD>
    </TR>
    <TR>
      <TD>WAN¦IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="rwanip" size="20" maxlength="15" value="$items{rwanip}" $readonly></TD>
    </TR>
    <TR>
      <TD>��⡼��IP���ɥ쥹</TD>
      <TD><INPUT type="text" name="rremoteip" size="20" maxlength="15" value="$items{rremoteip}" $readonly></TD>
    </TR>
    <TR>
      <TD>�ѥ��åȸ���³����</TD>
      <TD>$rpacketsel</TD>
    </TR>
    <TR>
      <TD>��������³����</TD>
      <TD>$rdialsel</TD>
    </TR>
	$receive_set
  </TBODY>
</TABLE>
	</TD></TR>
 </TBODY>
</TABLE>
<INPUT type="submit" name="btnSend" value="����" $disabled> 
<INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>
<A href="../html/subindex.html" target="_top">�ܺ������</A>
<INPUT type="submit" name="btnSetrestart" value="������¸�ȺƵ�ư�¹�" $disabled> 
</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %network = ();
	my %dhcp = ();
	my %wan = ();
	my %ddns = ();
	my %wan = ();
	my %items = ();
	my $i;

	#general����ƤӽФ�
	my $filename = &hyper::get_config_file("general");
	&hyper::add_section($filename,"" ,\%items, \%item_general, \%item_def_general);

	my $hs= `hostname`;
	$hs =~s/\r//g;
	$hs =~s/\n//g;
	$items{hostname} = $hs;

	# �����ե����뤬����м��Ф�
	$filename = &hyper::get_temp_file("general");
	&hyper::add_section($filename, "", \%items, \%item_general);

	#.serial�ե���������
	$filename = &hyper::get_fix_file(".serial");
	print "SERIAL = $filename\n";
	&hyper::add_section($filename, "", \%items, \%item_serial,\%item_def_serial);

	#.machine�ե���������
	$filename = &hyper::get_fix_file(".machine");
	&hyper::add_section($filename, "", \%items, \%item_machine,\%item_def_machine);

	#lan(network)�ե�����ƽ�
	%network = &hyper::get_section("network", "", \%item_network, \%$item_def_network);

	#DHCP����ƤӽФ�
	%dhcp = &hyper::get_section("dhcpsetup", "" ,\%item_dhcpsetup, \%item_def_dhcpsetup);
	# DHCP�꡼�����֤�ʬñ�̤��Ѵ�
	my $dtime = $dhcp{'dhcptime'} / 60;
	$dhcp{'dhcptime'} = "$dtime";

	#etc����ƤӽФ�
	%etc = &hyper::get_section("etcsetup", "", \%item_etcsetup, \%item_def_etcsetup);

	#ddns����ƤӽФ�
	%ddns = &hyper::get_section("ddnssetup", "", \%item_ddnssetup, \%item_def_ddnssetup);

	#wan����ƤӽФ�
	%wan = &hyper::get_section("wansetup", "", \%item_wansetup, \%item_def_wansetup);

	%items = (%items, %network, %dhcp, %etc, %ddns, %wan);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;
	my @Key;
	my %rhash = ();
	my $filename = "";

	#generalʬ�Τ�
	@Key = keys %item_general;
	%rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_general{$keyn}} = $items{"$keyn"};
	}
	$filename = &hyper::get_temp_file("general");
	&hyper::writefile_hush($filename, \%rhash);

	#lan(network)ʬ�Τ�
	@Key = keys %item_network;
	%rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_network{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("network");
	&hyper::writefile_hush($filename, \%rhash);

	#dhcpd
	@Key = keys %item_dhcpsetup;
	%rhash = ();
	foreach my $keyn (@Key) {
		if ($keyn eq 'dhcptime') {
		# ��ɽ�����Ѵ�
			$rhash{$item_dhcpsetup{$keyn}} = $items{"$keyn"} * 60;
		}
		else {
			$rhash{$item_dhcpsetup{$keyn}} = $items{"$keyn"};
		}
	}
	my $filename = &hyper::get_temp_file("dhcpsetup");
	&hyper::writefile_hush($filename, \%rhash);

	#etcsetupʬ�Τ�
	@Key = keys %item_etcsetup;
	%rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("etcsetup");
	&hyper::writefile_hush($filename, \%rhash);

	#ddnssetup
	@Key = keys %item_ddnssetup;
	%rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_ddnssetup{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("ddnssetup");
	&hyper::writefile_hush($filename, \%rhash);

	#wansetupʬ�Τ�
	@Key = keys %item_wansetup;
	%rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_wansetup{$keyn}} = $items{"$keyn"};
	}
	$filename = &hyper::get_temp_file("wansetup");
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

#�ѿ���������å�����
sub chk_graph {
	my ($str, $max) = @_;

	if($str eq ""){
		return 1;
	}
	if($str =~ /[^\x20-\x7e]/){
		return undef;
	}
	$len = length($str);
	if($len > $max) {
		return undef;
	}
	return 1;
}

sub opt_cidsel {
	my $value = $_[0];
	my @num   = ("0","1","2","3","4","5","6","7","8","9","10");
	my @type  = ("�����ֹ�","1","2","3","4","5","6","7","8","9","10");
	my $i;
	my $t;
	my $p = "<SELECT name=\"cid\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=cid value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=cid value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_typesel {
	my $value = $_[0];
	my @num   = ("1","2","3");
	my @type   = ("ȯ��/�忮 ξ��","ȯ���Τ�","�忮�Τ�");
	my $i;
	my $t;
	my $p = "<SELECT name=\"dialtype\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=dialtype value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=dialtype value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub rec_packetsel {
	my $value = $_[0];
	my @num   = ("0","1","2");
	my @type   = ("���Ƶ���","���Ƶ���","��ϿAPN�Τߵ���");
	my $i;
	my $t;
	my $p = "<SELECT name=\"rpacket\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=rpacket value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=rpacket value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub rec_dialsel {
	my $value = $_[0];
	my @num   = ("0","1","2");
	my @type   = ("���Ƶ���","���Ƶ���","��Ͽ�ֹ�Τߵ���");
	my $i;
	my $t;
	my $p = "<SELECT name=\"rdial\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=rdial value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=rdial value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_ddnssel {
	my $value = $_[0];
	my @num   = ("1","2");
	my @type   = ("Dynamic DO!.jp(̵��)","DynDNS.com");
	my $i;
	my $t;
	my $p = "<SELECT name=\"ddnsserver\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=ddnsserver value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=ddnsserver value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub pr_restart {
print "Content-Type:text/html\r\n\r\n";
print <<EOFRESTART;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<STYLE TYPE="text/css">
<!--
#barBG { position:absolute;left:0px; font-size:4px;
         background-color:#d0d0d0; width:210px; height:32px;}
#bar   { position:absolute;left:5px; font-size:4px;
         background-color:#808080; width:0px;   height:22px; }
#progTitle {}
#progMsg {}
--></STYLE>
<SCRIPT Language="JavaScript">
<!--
// �ץ��쥹�С�ɽ��
per   = 0;			// �ѡ�����ơ���
total = $restart_time;			// �ɤ߹���ȡ����������
//#barWidth = 200;	// �ץ��쥹�С��β���
function progressBar()
{
	wid = document.body.clientWidth;
	barWidth = wid-20;
	document.all["barBG"].style.width = barWidth+10;

	per++;
	w = (per / total) * barWidth;
	document.all["bar"].style.top   = document.all["barBG"].style.top+5;
	document.all["bar"].style.width = w;

	progTitle.innerText = "�Ƶ�ư��";
	var kaisu = total-per;
	progMsg.innerText = "��"+kaisu+"�ø�˺���³���Ƥ���������";

	if (per == total) setTimeout("hideProgressBar()",1000);
	else setTimeout('progressBar()',1000);
}
//�����÷вᤷ����ץ��쥹�С���õ�
function hideProgressBar()
{
	progTitle.innerText = "����³��ǽ�Ǥ���";
	document.all["progMsg"].style.visibility = "hidden";
	document.all["barBG"].style.visibility = "hidden";
}

// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="progressBar();">
<H2 align="center">$restitle</H2>
<CENTER>
<P><DIV ID="progTitle"></DIV></P>
<P><DIV ID="progMsg"></DIV></P>
</CENTER>
<P><DIV ID="barBG"><DIV ID="bar"></DIV></DIV></P>
</BODY>
</HTML>
EOFRESTART
}
