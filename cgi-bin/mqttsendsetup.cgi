#!/usr/bin/perl -w

require "hyper.pl";

%item_mqttsendsetup = (
 'log_onoff'            => "log_onoff",
 'logbuf_massive'       => "logbuf_massive",
 'logbuf_max'           => "logbuf_max",
 'logbuf_line'          => "logbuf_line",
 'status'               => "status",
 'status_time'          => "status_time",
 'databyte'             => "databyte",
 'latency'              => "latency",
 'latency_sel'          => "latency_sel",
 'ant'                  => "ant",
 'timediv'              => "timediv",
);

%item_def_mqttsendsetup = (
 'log_onoff'	        => "0",
 'logbuf_massive'       => "0",
 'logbuf_max'           => "",
 'logbuf_line'          => "1",
 'status'               => "0",
 'status_time'          => "",
 'databyte'             => "0",
 'latency'              => "0",
 'latency_sel'          => "1",
 'ant'                  => "0",
 'timediv'              => "0",
);

%error_list = (
 'timeinterror'      => "�ֳ�,�Կ��������ǻ��ꤷ�Ƥ���������",
 'timeerror'      => "�ֳ֤�10��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'maxerror'      => "�Կ���1��200�Ԥ��ϰϤǻ��ꤷ�Ƥ���������",
 'statuserror'      => "���ơ�����������ͭ���ˤ�����Ϻ�������������ƥ�Ĥ�ͭ���ˤ��Ƥ���������",
);

my $section = 'mqttsendsetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";


&hyper::get_args($commandline);			# ���������ؿ�

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_mqttsendsetup;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
	#�����Ȥ�����򵡼��̤������ȿ�Ǥ��롣

		&set_modify_item(%items);
	}
}
else {
	%items = &get_item();
}


sub chk_item {
	my %items = @_;

	if (($items{status} eq "1") && ($items{databyte} eq "0") && ($items{latency} eq "0") && ($items{ant} eq "0")) {
		return "statuserror";
	}

	if (($items{status_time} ne "") && (&hyper::checknumstring($items{status_time}) == 0)) {
		return "timeinterror";
	}

	if (($items{status_time} ne "") && (($items{status_time} < 10) || ($items{status_time} > 86400))) {
		return "timeerror";
	}

	if (($items{status} eq "1") && ($items{status_time} eq "")) {
		return "timeinterror";
	}

	if (($items{logbuf_max} ne "") && (&hyper::checknumstring($items{logbuf_max}) == 0)) {
		return "timeinterror";
	}

	if (($items{logbuf_max} ne "") && (($items{logbuf_max} < 1) || ($items{logbuf_max} > 200))) {
		return "maxerror";
	}

	if (($items{logbuf_massive} eq "1") && ($items{logbuf_max} eq "")) {
		return "timeinterror";
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
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0>$va_pr0";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1>$va_pr1";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value2\" $checked2>$va_pr2";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value3\" $checked3>$va_pr3";
	
	return $p;
}

sub set_input_pr{
	my ($n,$v,$s,$l,$en,$u) = @_;
	my $p = "";

	$p = "<INPUT size=\"$s\" type=\"text\" maxlength=\"$l\" name=\"$n\" value=\"$v\" $en>";
	$p = $p."��$u";

	return $p;
}


my $input_log = &set_radio_pr("log_onoff", $items{"log_onoff"}, "0", "1", "̵��", "ͭ��");
my $input_bufmassive = &set_radio_pr("logbuf_massive", $items{"logbuf_massive"}, "0", "1", "̵��", "ͭ��");
my $input_bufline = &set_radio_pr("logbuf_line", $items{"logbuf_line"}, "0", "1", "̵��", "ͭ��");
my $input_status = &set_radio_pr("status", $items{"status"}, "0", "1", "̵��", "ͭ��");
my $input_databyte = &set_radio_pr("databyte", $items{"databyte"}, "0", "1", "̵��", "ͭ��");
my $input_statustime = &set_input_pr("status_time", $items{"status_time"}, "10", "5","","�ôֳ�");
my $input_bufmax = &set_input_pr("logbuf_max", $items{"logbuf_max"}, "10", "5","","��(����)");
my $input_latency = &set_radio_pr("latency", $items{"latency"}, "0", "1", "̵��", "ͭ��");
my $input_ant = &set_radio_pr("ant", $items{"ant"}, "0", "1", "̵��", "ͭ��");
my $input_timediv = &set_radio_pr("timediv", $items{"timediv"}, "0", "1", "̵��", "ͭ��");
my $optlatencysel = &opt_latencysel($items{"latency_sel"});

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
<H2>��������</H2>
<FORM name="mqttsendsetup" action="./mqttsendsetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">���ߥ顼���</TD>
     <TD colspan="2">$input_log</TD>
    </TR>
    <TR>
     <TD width="200">��PPP̤��³���Υ�</TD>
     <TD colspan="2">��</TD>
    </TR>
    <TR>
     <TD width="200">�����������</TD>
     <TD width="170">$input_bufmassive</TD>
     <TD width="220">$input_bufmax</TD>
    </TR>
    <TR>
     <TD width="200">������ñ������</TD>
     <TD width="170">$input_bufline</TD>
     <TD colspan="3">��</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="200">����ƥ������</TD>
     <TD width="170">$input_status</TD>
     <TD>$input_statustime</TD>
    </TR>   

    <TR>
     <TD width="200">���������Х��ȿ�(WAN¦)</TD>
     <TD width="170">$input_databyte</TD>
     <TD colspan="3">��</TD>
    </TR>   

    <TR>
     <TD width="200">���̿��쥤�ƥ󥷡�</TD>
     <TD width="170">$input_latency</TD>
     <TD width="200">$optlatencysel</TD>
    </TR>   

    <TR>
     <TD width="200">�����ȼ�������</TD>
     <TD width="170">$input_ant</TD>
     <TD colspan="3">��</TD>
    </TR>   

    <TR>
     <TD width="200">������ʬ��ե����ޥå�</TD>
     <TD width="170">$input_timediv</TD>
     <TD colspan="3">��</TD>
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
	%items = &hyper::get_section($section, "", \%item_mqttsendsetup, \%item_def_mqttsendsetup);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_mqttsendsetup;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_mqttsendsetup{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file($section);
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

sub opt_latencysel {
        my $value = $_[0];
        my @num   = ("1","2","3","4","5");
        my @type   = ("��³�ƻ�(WAN����)","Ping�ˤ����³�ƻ뵡ǽ(WAN¦)","Ping�ˤ����³�ƻ뵡ǽ(LAN¦)","Ping�ˤ����³�ƻ뵡ǽ(LAN¦2)","Ping�ˤ����³�ƻ뵡ǽ(VPN¦)");
        my $i;
        my $t;
        my $p = "<SELECT name=\"latency_sel\">";
        foreach my $i (@num) {
                $t = shift @type;
                if ($i eq $value) {
                        $p = $p."<OPTION name=latency_sel value=\"$i\" selected>$t</OPTION>\n";
                }
                else {
                        $p = $p."<OPTION name=latency_sel value=\"$i\">$t</OPTION>\n";
                }
        }
        $p = $p."</SELECT>\n";
        return $p;
}

