#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_etcsetup = (
 'icmp'      => "icmp",
 'virtserve' => "virtserve",
 'virtip'    => "virtip",
 'reboot'    => "reboot",
 'reboot_time'    => "reboot_time",
 'pingcheck'    => "pingcheck",
 'ipdomain'    => "ipdomain",
 'pingip'    => "pingip",
 'sleep_time'    => "sleep_time",
 'errorcount'    => "errorcount",
 'pingcheck2'    => "pingcheck2",
 'pingip2'    => "pingip2",
 'sleep_time2'    => "sleep_time2",
 'errorcount2'    => "errorcount2",
 'pingcheck3'    => "pingcheck3",
 'pingip3'    => "pingip3",
 'pinglocalip3'    => "pinglocalip3",
 'sleep_time3'    => "sleep_time3",
 'errorcount3'    => "errorcount3",
 'pingcheck4'    => "pingcheck4",
 'pingip4'    => "pingip4",
 'sleep_time4'    => "sleep_time4",
 'errorcount4'    => "errorcount4",
);

%item_def_etcsetup = (
 'icmp'      => "1",
 'virtserve' => "0",
 'virtip'    => "",
 'reboot'    => "0",
 'reboot_time'    => "86400",
 'pingcheck'    => "0",
 'ipdomain'    => "0",
 'pingip'    => "",
 'sleep_time'    => "60",
 'errorcount'    => "3",
 'pingcheck2'    => "0",
 'pingip2'    => "",
 'sleep_time2'    => "60",
 'errorcount2'    => "3",
 'pingcheck3'    => "0",
 'pingip3'    => "",
 'pinglocalip3'    => "",
 'sleep_time3'    => "60",
 'errorcount3'    => "3",
 'pingcheck4'    => "0",
 'pingip4'    => "",
 'sleep_time4'    => "60",
 'errorcount4'    => "3",
);

%item_list = (%item_etcsetup);
%item_def  = (%item_def_etcsetup);

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Location: ./general.cgi\n\n";
}

my $readonly ="";
my $disabled ="";
my $section = 'etcsetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";

%error_list = (
 'ipadrerror'     => "�С�����륵����������IP���ɥ쥹�����꤬����������ޤ���",
 'pingipadrerror'     => "Ping������IP���ɥ쥹�����꤬����������ޤ���",
 'pingdomainerror'     => "Ping������ɥᥤ��̾�����꤬����������ޤ���",
 'pingtimeinterror'     => "�����ֳ֤������ǻ��ꤷ�Ʋ�������",
 'pingtimeerror'     => "�����ֳ֤�10����86400�äδ֤ǻ��ꤷ�Ʋ�������",
 'reboottimeerror'     => "��֡��ȴֳ֤�600����8640000�äδ֤ǻ��ꤷ�Ʋ�������",
);

&hyper::get_args($commandline);			# ���������ؿ�

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
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
else {
	%items = &get_item();
}

my $tlist1 = init_list1(%items);
my $tlist2 = init_list2(%items);
my $tlist3 = init_list3(%items);
my $tlist4 = init_list4(%items);
my $tlist5 = init_list5(%items);
my $tlist6 = init_list6(%items);
my $tlist7 = init_list7(%items);
my $tlist8 = init_list8(%items);
my $tlist9 = init_list9(%items);
my $tlist10 = init_list10(%items);

#
#ICMP���������ꤹ��
#
sub init_list1 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{icmp}" eq "1") {
	$p = <<"ICMPON";
	  <TD width="100"><input type="radio" name="icmp" value="0" >��������</TD>
	  <TD width="100"><input type="radio" name="icmp" value="1" checked>�롼������</TD>
ICMPON
	}
	else {
	$p = <<"ICMPOFF";
	  <TD width="100"><input type="radio" name="icmp" value="0" checked>��������</TD>
	  <TD width="100"><input type="radio" name="icmp" value="1">�롼������</TD>
ICMPOFF
	}
	return $p;
}

#
#�С�����륵���С���ǽ�����ꤹ��
#
sub init_list2 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{virtserve}" eq "1") {
	$p = <<"VIRTON";
	  <TD width="100"><input type="radio" name="virtserve" value="0">̵��</TD>
	  <TD width="100"><input type="radio" name="virtserve" value="1" checked>ͭ��</TD>
VIRTON
	}
	else {
	$p = <<"VIRTOFF";
	  <TD width="100"><input type="radio" name="virtserve" value="0" checked>̵��</TD>
	  <TD width="100"><input type="radio" name="virtserve" value="1">ͭ��</TD>
VIRTOFF
	}
	return $p;
}

#
#��³�ƻ뵡ǽ�����ꤹ��
#
sub init_list3 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{pingcheck}" eq "1") {
	$p = <<"PINGON";
	  <TD width="100"><input type="radio" name="pingcheck" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck" value="1" checked>ON</TD>
PINGON
	}
	else {
	$p = <<"PINGOFF";
	  <TD width="100"><input type="radio" name="pingcheck" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck" value="1">ON</TD>
PINGOFF
	}
	return $p;
}

sub init_list4 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{ipdomain}" eq "1") {
	$p = <<"IP";
	  <TD width="100"><input type="radio" name="ipdomain" value="0" >IP���ɥ쥹</TD>
	  <TD width="100"><input type="radio" name="ipdomain" value="1" checked>�ɥᥤ��̾</TD>
IP
	}
	else {
	$p = <<"DOMAIN";
	  <TD width="100"><input type="radio" name="ipdomain" value="0" checked>IP���ɥ쥹</TD>
	  <TD width="100"><input type="radio" name="ipdomain" value="1">�ɥᥤ��̾</TD>
DOMAIN
	}
	return $p;
}

#
#��³�ƻ뵡ǽ(LAN¦)�����ꤹ��
#
sub init_list5 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{pingcheck2}" eq "1") {
	$p = <<"PINGON2";
	  <TD width="100"><input type="radio" name="pingcheck2" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck2" value="1" checked>ON</TD>
PINGON2
	}
	else {
	$p = <<"PINGOFF2";
	  <TD width="100"><input type="radio" name="pingcheck2" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck2" value="1">ON</TD>
PINGOFF2
	}
	return $p;
}


#
#��³�ƻ뵡ǽ(LAN¦��)�����ꤹ��
#
sub init_list10 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{pingcheck4}" eq "1") {
	$p = <<"PINGON4";
	  <TD width="100"><input type="radio" name="pingcheck4" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck4" value="1" checked>ON</TD>
PINGON4
	}
	else {
	$p = <<"PINGOFF4";
	  <TD width="100"><input type="radio" name="pingcheck4" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck4" value="1">ON</TD>
PINGOFF4
	}
	return $p;
}

#
#�����֡��ȵ�ǽ�����ꤹ��
#
sub init_list6 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{reboot}" eq "1") {
	$p = <<"REBOOTON";
	  <TD width="100"><input type="radio" name="reboot" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="reboot" value="1" checked>ON</TD>
REBOOTON
	}
	else {
	$p = <<"REBOOTOFF";
	  <TD width="100"><input type="radio" name="reboot" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="reboot" value="1">ON</TD>
REBOOTOFF
	}
	return $p;
}

#
#��³�ƻ뵡ǽ(VPN¦)�����ꤹ��
#
sub init_list7 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{pingcheck3}" eq "1") {
	$p = <<"PINGON3";
	  <TD width="100"><input type="radio" name="pingcheck3" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck3" value="1" checked>ON</TD>
PINGON3
	}
	else {
	$p = <<"PINGOFF3";
	  <TD width="100"><input type="radio" name="pingcheck3" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="pingcheck3" value="1">ON</TD>
PINGOFF3
	}
	return $p;
}

#
#�����å��ɥå�Ϣư(VPN¦)�����ꤹ��
#
sub init_list8 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{watchdog3}" eq "1") {
	$p = <<"WATCHDOGON3";
	  <TD width="100"><input type="radio" name="watchdog3" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="watchdog3" value="1" checked>ON</TD>
WATCHDOGON3
	}
	else {
	$p = <<"WATCHDOGOFF3";
	  <TD width="100"><input type="radio" name="watchdog3" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="watchdog3" value="1">ON</TD>
WATCHDOGOFF3
	}
	return $p;
}

#
#�����å��ɥå�Ϣư(WAN¦)�����ꤹ��
#
sub init_list9 {
	my %items = @_;#item�ǡ���
	my $p = "";

	if ("$items{watchdog}" eq "1") {
	$p = <<"WATCHDOGON";
	  <TD width="100"><input type="radio" name="watchdog" value="0" >OFF</TD>
	  <TD width="100"><input type="radio" name="watchdog" value="1" checked>ON</TD>
WATCHDOGON
	}
	else {
	$p = <<"WATCHDOGOFF";
	  <TD width="100"><input type="radio" name="watchdog" value="0" checked>OFF</TD>
	  <TD width="100"><input type="radio" name="watchdog" value="1">ON</TD>
WATCHDOGOFF
	}
	return $p;
}


sub chk_item {
	my %items = @_;

	if (($items{virtserve} eq "1") || ($items{virtip} ne "")) {
		if (&hyper::get_ipaddress($items{virtip}) eq "") {
			return "ipadrerror";
		}
	}
	if (($items{pingcheck} eq "1") || ($items{pingip} ne "")) {
	if ($items{ipdomain} eq "0") {
		if (&hyper::get_ipaddress($items{pingip}) eq "") {
			return "pingipadrerror";
		}
	}else{
		if ((&hyper::chk_graph($items{pingip}, 64) eq "") || ($items{pingip} eq "")) {
			return "pingdomainerror";
		}
	}
	}
	if (&hyper::checknumstring($items{sleep_time}) == 0) {
		return "pingtimeinterror";
	}
	if (($items{sleep_time} < 10) || ($items{sleep_time} > 86400)) {
		return "pingtimeerror";
	}
	if (($items{pingcheck2} eq "1") || ($items{pingip2} ne "")) {
		if (&hyper::get_ipaddress($items{pingip2}) eq "") {
			return "pingipadrerror";
		}
	}
	if (&hyper::checknumstring($items{sleep_time2}) == 0) {
		return "pingtimeinterror";
	}
	if (($items{sleep_time2} < 10) || ($items{sleep_time2} > 86400)) {
		return "pingtimeerror";
	}
	if (($items{pingcheck4} eq "1") || ($items{pingip4} ne "")) {
		if (&hyper::get_ipaddress($items{pingip4}) eq "") {
			return "pingipadrerror";
		}
	}
	if (&hyper::checknumstring($items{sleep_time4}) == 0) {
		return "pingtimeinterror";
	}
	if (($items{sleep_time4} < 10) || ($items{sleep_time4} > 86400)) {
		return "pingtimeerror";
	}
	if (($items{pingcheck3} eq "1") || ($items{pingip3} ne "")) {
		if (&hyper::get_ipaddress($items{pingip3}) eq "") {
			return "pingipadrerror";
		}
	}
	if (($items{pingcheck3} eq "1") || ($items{pinglocalip3} ne "")) {
		if (&hyper::get_ipaddress($items{pinglocalip3}) eq "") {
			return "pingipadrerror";
		}
	}
	if (&hyper::checknumstring($items{sleep_time3}) == 0) {
		return "pingtimeinterror";
	}
	if (($items{sleep_time3} < 10) || ($items{sleep_time3} > 86400)) {
		return "pingtimeerror";
	}
	if (&hyper::checknumstring($items{reboot_time}) == 0) {
		return "pingtimeinterror";
	}
	if (($items{reboot_time} < 600) || ($items{reboot_time} > 8640000)) {
		return "reboottimeerror";
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

sub get_item {
	my %items = ();
	my $i;

	#general����ƤӽФ�
	my $filename = &hyper::get_config_file("etcsetup");
	&hyper::add_section($filename,"" ,\%items, \%item_list, \%item_def);

	# �����ե����뤬����м��Ф�
	$filename = &hyper::get_temp_file("etcsetup");
	&hyper::add_section($filename, "", \%items, \%item_list);

	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_list;#generalʬ�Τ�
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("etcsetup");
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

my $opterrorcountsel = &opt_errorcountsel($items{"errorcount"});
my $opterrorcountsel2 = &opt_errorcountsel2($items{"errorcount2"});
my $opterrorcountsel3 = &opt_errorcountsel3($items{"errorcount3"});
my $opterrorcountsel4 = &opt_errorcountsel4($items{"errorcount4"});

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 10.0.1.0 for Windows">
<TITLE></TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
$err_item
<H2>����¾����</H2>
<FORM action="./etcsetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="230">ICMP����</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist1</TR></TBODY></TABLE></TD>
    </TR>
    <TR>
      <TD width="230">�С�����륵���е�ǽ</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist2</TR></TBODY></TABLE></TD>
    </TR>
    <TR>
      <TD width="250">�С�����륵����������IP���ɥ쥹</TD>
      <TD><INPUT size="31" type="text" maxlength="15" name="virtip" value="$items{virtip}" $readonly></TD>
    </TR>
    <TR>
      <TD width="230">�����֡��ȵ�ǽ</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist6</TR></TBODY></TABLE></TD>
    </TR>
    <TR>
      <TD>��֡��ȴֳ�</TD>
      <TD><INPUT type="text" name="reboot_time" size="31" maxlength="7" value="$items{reboot_time}" $readonly>��</TD>
    </TR>
  </TBODY>
</TABLE>
<BR>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="230">Ping�ˤ����³�ƻ뵡ǽ(WAN¦)</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist3</TR></TBODY></TABLE></TD>
    </TR>
<!--
    <TR>
      <TD width="230">�����å��ɥå�Ϣư</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist9</TR></TBODY></TABLE></TD>
    </TR>
-->
    <TR>
      <TD width="230">�����������ˡ</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist4</TR></TBODY></TABLE></TD>
    </TR>
    <TR>
      <TD width="250">�����襢�ɥ쥹</TD>
      <TD><INPUT size="31" type="text" maxlength="64" name="pingip" value="$items{pingip}" $readonly></TD>
    </TR>
    <TR>
      <TD>�����ֳ�</TD>
      <TD><INPUT type="text" name="sleep_time" size="31" maxlength="5" value="$items{sleep_time}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>Ϣ³���顼Ƚ����</TD>
      <TD width="150">$opterrorcountsel</TD>
    </TR>
  </TBODY>
</TABLE>
<BR>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="230">Ping�ˤ����³�ƻ뵡ǽ(LAN¦)</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist5</TR></TBODY></TABLE></TD>
    </TR>
    <TR>
      <TD width="250">�����襢�ɥ쥹</TD>
      <TD><INPUT size="31" type="text" maxlength="64" name="pingip2" value="$items{pingip2}" $readonly></TD>
    </TR>
    <TR>
      <TD>�����ֳ�</TD>
      <TD><INPUT type="text" name="sleep_time2" size="31" maxlength="5" value="$items{sleep_time2}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>Ϣ³���顼Ƚ����</TD>
      <TD width="150">$opterrorcountsel2</TD>
    </TR>
  </TBODY>
</TABLE>
<BR>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="230">Ping�ˤ����³�ƻ뵡ǽ(LAN¦2)</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist10</TR></TBODY></TABLE></TD>
    </TR>
    <TR>
      <TD width="250">�����襢�ɥ쥹</TD>
      <TD><INPUT size="31" type="text" maxlength="64" name="pingip4" value="$items{pingip4}" $readonly></TD>
    </TR>
    <TR>
      <TD>�����ֳ�</TD>
      <TD><INPUT type="text" name="sleep_time4" size="31" maxlength="5" value="$items{sleep_time4}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>Ϣ³���顼Ƚ����</TD>
      <TD width="150">$opterrorcountsel4</TD>
    </TR>
  </TBODY>
</TABLE>
<BR>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD width="230">Ping�ˤ����³�ƻ뵡ǽ(VPN¦)</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist7</TR></TBODY></TABLE></TD>
    </TR>
<!--
    <TR>
      <TD width="230">�����å��ɥå�Ϣư</TD>
        <TD><TABLE border="0"><TBODY><TR>$tlist8</TR></TBODY></TABLE></TD>
    </TR>
-->
    <TR>
      <TD width="250">�����襢�ɥ쥹</TD>
      <TD><INPUT size="31" type="text" maxlength="64" name="pingip3" value="$items{pingip3}" $readonly></TD>
    </TR>
    <TR>
      <TD width="250">VPN������¦���ɥ쥹</TD>
      <TD><INPUT size="31" type="text" maxlength="64" name="pinglocalip3" value="$items{pinglocalip3}" $readonly></TD>
    </TR>
    <TR>
      <TD>�����ֳ�</TD>
      <TD><INPUT type="text" name="sleep_time3" size="31" maxlength="5" value="$items{sleep_time3}" $readonly>��</TD>
    </TR>
    <TR>
      <TD>Ϣ³���顼Ƚ����</TD>
      <TD width="150">$opterrorcountsel3</TD>
    </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML

sub opt_errorcountsel {
	my $value = $_[0];
	my @num   = ("1","2","3","4","5","6","7","8","9","10");
	my @type   = ("1","2","3","4","5","6","7","8","9","10");
	my $i;
	my $t;
	my $p = "<SELECT name=\"errorcount\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=errorcount value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=errorcount value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_errorcountsel2 {
	my $value = $_[0];
	my @num   = ("1","2","3","4","5","6","7","8","9","10");
	my @type   = ("1","2","3","4","5","6","7","8","9","10");
	my $i;
	my $t;
	my $p = "<SELECT name=\"errorcount2\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=errorcount2 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=errorcount2 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_errorcountsel3 {
	my $value = $_[0];
	my @num   = ("1","2","3","4","5","6","7","8","9","10");
	my @type   = ("1","2","3","4","5","6","7","8","9","10");
	my $i;
	my $t;
	my $p = "<SELECT name=\"errorcount3\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=errorcount3 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=errorcount3 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_errorcountsel4 {
	my $value = $_[0];
	my @num   = ("1","2","3","4","5","6","7","8","9","10");
	my @type   = ("1","2","3","4","5","6","7","8","9","10");
	my $i;
	my $t;
	my $p = "<SELECT name=\"errorcount4\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=errorcount4 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=errorcount4 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

