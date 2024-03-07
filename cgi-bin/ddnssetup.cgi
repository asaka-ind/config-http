#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

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

%error_list = (
 'ddnsnameerror'     => "�����ʥߥå�DNS�ɥᥤ��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'ddnsusererror'     => "�����ʥߥå�DNS�桼��̾��Ⱦ�ѱѿ���64ʸ������ǻ��ꤷ�Ƥ���������",
 'ddnspasswderror'   => "�����ʥߥå�DNS�ѥ���ɤ�Ⱦ�ѱѿ���20ʸ������ǻ��ꤷ�Ƥ���������",
);

my $section = 'ddnssetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $ddns_onoff ="";

&hyper::get_args($commandline);			# ���������ؿ�

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_ddnssetup;
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

$ddns_onoff = input_ddns($items{ddns_onoff});

sub chk_item {
	my %items = @_;

	if (&chk_graph($items{ddnsname}, 64) eq "" ) {
		return "ddnsnameerror";
	}

	if (&chk_graph($items{ddnsuser}, 64) eq "" ) {
		return "ddnsusererror";
	}

	if (&chk_graph($items{ddnspasswd}, 20) eq "" ) {
		return "ddnspasswderror";
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

sub input_ddns {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"ddns_onoff\" value=\"0\" checked>OFF  <INPUT type=\"radio\" name=\"ddns_onoff\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"ddns_onoff\" value=\"0\" >OFF  <INPUT type=\"radio\" name=\"ddns_onoff\" value=\"1\" checked>ON";
	}
	return $p;
}

my $readonly ="";
my $disabled ="";
if (!&hyper::get_logincheck()) {
	$disabled = "disabled";
	$readonly = "readonly";
}

my $optddnssel = &opt_ddnssel($items{"ddnsserver"});

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
<H2>�����ʥߥå�DNS����</H2>
<FORM name="ddnssetup" action="./ddnssetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD>�����ʥߥå�DNS</TD>
     <TD>$ddns_onoff</TD>
    </TR>
   
    <TR>
      <TD>�����ʥߥå�DNS������</TD>
      <TD width="150">$optddnssel</TD>
    </TR>

    <TR>
      <TD>�ɥᥤ��̾</TD>
      <TD><INPUT type="text" name="ddnsname" size="31" maxlength="64" value="$items{ddnsname}" $readonly></TD>
    </TR>

    <TR>
      <TD>�桼��̾</TD>
      <TD><INPUT type="text" name="ddnsuser" size="31" maxlength="64" value="$items{ddnsuser}" $readonly></TD>
    </TR>
    <TR>
      <TD>�ѥ����</TD>
      <TD><INPUT type="password" name="ddnspasswd" size="31" maxlength="20" value="$items{ddnspasswd}" $readonly></TD>
    </TR>
<!--
    <TR>
      <TD>DNS������IP(�ץ饤�ޥ�)</TD>
      <TD><INPUT type="text" name="dhcpdns1" size="31" maxlength="15" value="$items{dhcpdns1}" $readonly></TD>
    </TR>
    <TR>
      <TD>DNS������IP(���������)</TD>
      <TD><INPUT type="text" name="dhcpdns2" size="31" maxlength="15" value="$items{dhcpdns2}" $readonly></TD>
    </TR>
-->
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %items = ();
	#g����ƤӽФ�
	%items = &hyper::get_section($section, "", \%item_ddnssetup, \%item_def_ddnssetup);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_ddnssetup;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_ddnssetup{$keyn}} = $items{"$keyn"};
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

sub opt_ddnssel {
	my $value = $_[0];
	my @num   = ("1","2","3","4");
	my @type   = ("Dynamic DO!.jp(̵��)","DynDNS.com","Dynamic DO!.jp(ͭ��)","ind-ddns.com");
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

