#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/vpn.pl";

%item_list = ();
%item_def = ();

my $list_count = &vpn::get_list_count();

my $commandline = "";
my %items = ();
my $setting = "";
my $retrying = "";
my $Readfile = "";
my $Writefile = "";
my $ConfFile = "";
my $err_item ="";
my $number = 0;
my $type = "";
my $section = "vpnsetup";

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

&vpn::make_list(\%item_list, \%item_def);

%error_list = (
 'nameerror'      => "��³̾�Τϱѿ���16ʸ����������ꤷ�Ƥ���������",
 'name2error'      => "��³̾�Τ�Ʊ��̾��������ޤ���",
 'name3error'      => "��³̾�Τϥ���ե��٥å�(a-zA-Z)�ǻϤޤ�ʤ���Ф����ޤ���",
 'ladipseterror'      => "�����륢�ɥ쥹��IP����Ǥ�IP���ɥ쥹�����ꤷ�Ƥ���������",
 'ladiperror'      => "�����륢�ɥ쥹�����꤬����������ޤ��󡣡��㡧192.168.10.100)",
 'lsubseterror'      => "�����륵�֥ͥåȥ��ɥ쥹����Ѥ���Ǥ�IP���ɥ쥹�����ꤷ�Ƥ���������",
 'lsuberror'      => "�����륵�֥ͥåȥ��ɥ쥹�����꤬����������ޤ��󡣡��㡧192.168.10.100/24 �ޤ��ϡ�192.168.10.100/255.255.255.0��",
 'liderror'      => "������ID�ϱѿ���16ʸ����������ꤷ�Ƥ���������",
 'lhopseterror'      => "������ͥ����ȥۥåץ��ɥ쥹�����ꤷ�Ƥ���������",
 'lhoperror'      => "������ͥ���ȥۥåץ��ɥ쥹�����꤬����������ޤ��󡣡��㡧192.168.10.100)",
 'radipseterror'      => "��⡼�ȥ��ɥ쥹��IP����Ǥ�IP���ɥ쥹�����ꤷ�Ƥ���������",
 'raddnseterror'      => "��⡼�ȥ��ɥ쥹�Υɥᥤ��̾����Ǥϥɥᥤ��̾�����ꤷ�Ƥ���������",
 'radiperror'      => "��⡼�ȥ��ɥ쥹��IP��������꤬����������ޤ��󡣡��㡧192.168.10.100)",
 'raddnerror'      => "��⡼�ȥ��ɥ쥹�Υɥᥤ��̾����ϱѿ���64ʸ����������ꤷ�Ƥ���������",
 'raderror'      => "��⡼�ȥ��ɥ쥹�ϱѿ���64ʸ����������ꤷ�Ƥ���������",
 'rsubseterror'      => "��⡼�ȥ��֥ͥåȥ��ɥ쥹����Ѥ���Ǥ�IP���ɥ쥹�����ꤷ�Ƥ���������",
 'rsuberror'      => "��⡼�ȥ��֥ͥåȥ��ɥ쥹�����꤬����������ޤ��󡣡��㡧192.168.10.100/24 �ޤ��ϡ�192.168.10.100/255.255.255.0��",
 'riderror'      => "��⡼��ID�ϱѿ���16ʸ����������ꤷ�Ƥ���������",
 'pskerror'      => "��ͭ���ϱѿ���32ʸ����������ꤷ�Ƥ���������",
 'rsaerror'      => "��ͭ�����ͤ������ͤǤ���",
 'ikeseterror'      => "�Ź������ե�����1�Ǥ���¾�ΤȤ��ϡ��Ź������������Ƥ���������",
 'ikeerror'      => "�Ź������ե�����1�����꤬����������ޤ���",
 'espseterror'      => "�Ź������ե�����2�Ǥ���¾�ΤȤ��ϡ��Ź������������Ƥ���������",
 'esperror'      => "�Ź������ե�����2�����꤬����������ޤ���",
 'keymgerror'      => "���򴹤Υޡ������30��3600�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'keytmerror'      => "���μ�̿��0��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'dpddelayerror'      => "DPD�����ֳ֤�5��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'dpdtmerror'      => "DPD�����ॢ���Ȥ�5��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'satmerror'      => "SA�μ�̿��0��28800�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'keylssaerror' => "���μ�̿�ϡ�SA�μ�̿�ʾ���ͤ���ꤷ�Ƥ���������",
 'salskeymgerror' => "SA�μ�̿�ϸ��򴹤Υޡ������2�ܰʾ�ǻ��ꤷ�Ƥ���������",
);
&hyper::get_args($commandline);			# ���������ؿ�
#$commandline="btnRead=1&type=view";

if ( ! defined $commandline) {
#�������ʤ��Ȥ��Ͻ�λ
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

$commandline = hyper::url_decode($commandline);
#$type = &hyper::get_param("type", $commandline);
$setting = &hyper::get_param("btnSet", $commandline);
$retrying = &hyper::get_param("btnRetry", $commandline);
$number = &hyper::get_param("number", $commandline);
$Readfile = &hyper::get_param("btnRead", $commandline);
$Writefile = &hyper::get_param("btnWrite", $commandline);
$ConfFile = &hyper::get_param("confFile", $commandline);

if(! defined $number){

	
	for ($i = 1; $i <= $list_count; $i++) {
		 my $modnum = &hyper::get_param("btnModify$i" , $commandline);

		if(defined $modnum){ 
			$number = $i;
			last;
		 }
	}
}


if (! defined $number) {
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

%items = &hyper::get_section("vpnsetup", "" ,\%item_list, \%item_def);


if (defined $setting) {

	#checkbox
	$items{"vpn_pfs$number"} = "";

	my @Keys = keys %item_list;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	if( $items{"vpn_pfs$number"} eq "") {$items{"vpn_pfs$number"} = "no"; }

	$err_item = &chk_item(\%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {


		&set_modify_item(%items);
		print "Status: 302 Moved\n";
		print "Location: ./vpn.cgi\n\n";
		#exit;
	}
}
elsif (defined $Readfile) {
	&set_fileout_item(%items);
	exit
}
elsif (defined $Writefile) {
	&set_filein_item(\%items);
}
else {
=pod
	print "Location: ./general.cgi\n\n";
=cut
}

sub set_fileout_item {
	my %items = @_;

	my @Key = &vpn::get_item_vpnsetn();
	my $pr = "";
	foreach my $keyn (@Key) {
		my $p = "$keyn=$items{\"vpn_$keyn$number\"}\r\n";
		$pr = $pr.$p;
	}
#	my $filename ="../../../var/conffile/file.conf";
#	&hyper::writefile($filename, $pr);

	my $default_name = "$items{\"vpn_name$number\"}.conf";
	print "Content-type: application/download\n";
	print "Content-disposition: attachment; filename=\"$default_name\"\n\n";
	print $pr;
}

sub set_filein_item {
	my ($it) = @_;

	my $filename = &vpn::get_conf_file();
	my %hashs = ();
	%hashs = &hyper::readfile_hash($filename);

	my @Key = &vpn::get_item_vpnsetn();
	foreach my $keyn (@Key) {
		if ( exists $hashs{"$keyn"}){
			$it->{"vpn_$keyn$number"} = $hashs{"$keyn"};
		}
	}
}

sub set_modify_item {
	my %items = @_;

	my @Key = keys %item_list;#
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("vpnsetup");
	&hyper::writefile_hush($filename, \%rhash);
}

sub chk_item {
	my $it = $_[0];
	my $i = 0;

	if ($it->{"vpn_name$number"} eq "" ) {
		return "nameerror";
	}
	if (&hyper::chk_graph($it->{"vpn_name$number"}, 16) eq "" ) {
		return "nameerror";
	}
	if (&hyper::chk_initial($it->{"vpn_name$number"}, 16) eq "" ) {
		return "name3error";
	}
	for ($i = 1; $i <= $list_count; $i++) {
		if($number != $i && $it->{"vpn_name$number"}  eq $it->{"vpn_name$i"} ){
			return "name2error";
		}
	}
	#lad
	if(($it->{"vpn_ladsel$number"} eq "1") && (! length $it->{"vpn_lad$number"})) {
		return "ladipseterror";
	}	
	if ((length $it->{"vpn_lad$number"}) && (&hyper::get_ipaddress($it->{"vpn_lad$number"}, 1) eq "")) {
		return "ladiperror";
	}
	#lsub
	if(($it->{"vpn_lsubsel$number"} eq "1") && (! length $it->{"vpn_lsub$number"})) {
		return "lsubseterror";
	}
	if ((length $it->{"vpn_lsub$number"}) && (&vpn::get_subnetaddress($it->{"vpn_lsub$number"}, 1) eq "")) {
		return "lsuberror";
	}
	#lid
	if (&hyper::chk_graph($it->{"vpn_lid$number"}, 16) eq "" ) {
		return "liderror";
	}
	#lhop
	if (($it->{"vpn_lhopsel$number"} eq "1") && (! length $it->{"vpn_lhop$number"})) {
			return "lhopseterror";
	}
	if ((length $it->{"vpn_lhop$number"}) && (&hyper::get_ipaddress($it->{"vpn_lhop$number"}, 1) eq "")) {
			return "lhoperror";
	}

	#rad
	if($it->{"vpn_radsel$number"} eq "1") {
		if (! length $it->{"vpn_rad$number"}) {
			return "radipseterror";
		}elsif  (&hyper::get_ipaddress($it->{"vpn_rad$number"}, 1) eq "") {
			return "radiperror";
		}
	}elsif ($it->{"vpn_radsel$number"} eq "2") {
		if (! length $it->{"vpn_rad$number"}) {
			return "raddnseterror";
		}elsif  (&hyper::chk_graph($it->{"vpn_rad$number"}, 64) eq "" ) {
			return "raddnerror";
		}
	}else{
		if  (&hyper::chk_graph($it->{"vpn_rad$number"}, 64) eq "" ) {
			return "raderror";
		}
	}
	#rsub
	if(($it->{"vpn_rsubsel$number"} eq "1") && (! length $it->{"vpn_rsub$number"})) {
		return "rsubseterror";
	}
	if ((length $it->{"vpn_rsub$number"}) && (&vpn::get_subnetaddress($it->{"vpn_rsub$number"}, 1) eq "")) {
		return "rsuberror";
	}
	#rid
	if (&hyper::chk_graph($it->{"vpn_rid$number"}, 16) eq "" ) {
		return "riderror";
	}
	#psk
	if (&hyper::chk_graph($it->{"vpn_psk$number"}, 32) eq "" ) {
		return "pskerror";
	}
	#rsa
	if (&hyper::chk_graph($it->{"vpn_rsa$number"}, 600) eq "" ) {
		return "rsaerror";
	}
	#ike
	if(($it->{"vpn_ikesel$number"} eq "3") && (! length $it->{"vpn_ike$number"})) {
		return "ikeseterror";
	}
	if ((length $it->{"vpn_ike$number"}) && (&hyper::chk_graph($it->{"vpn_ike$number"}, 32) eq "" )) {
		return "ikeerror";
	}
	#esp
	if(($it->{"vpn_espsel$number"} eq "3") && (! length $it->{"vpn_esp$number"})) {
		return "espseterror";
	}
	if ((length $it->{"vpn_esp$number"}) && (&hyper::chk_graph($it->{"vpn_esp$number"}, 32) eq "" )) {
		return "esperror";
	}
	#kyemg
	if (&hyper::checknumstring($it->{"vpn_keymg$number"}) == 0) {
		return "keymgerror";
	}
	if (($it->{"vpn_keymg$number"} < 30) || ($it->{"vpn_keymg$number"} > 3600)) {
		return "keymgerror";
	}
	#kyetm
	if (&hyper::checknumstring($it->{"vpn_keytm$number"}) == 0) {
		return "keytmerror";
	}
	if (($it->{"vpn_keytm$number"} < 0) || ($it->{"vpn_keytm$number"} > 86400)) {
		return "keytmerror";
	}
	#satm
	if (&hyper::checknumstring($it->{"vpn_satm$number"}) == 0) {
		return "satmerror";
	}
	if (($it->{"vpn_satm$number"} < 0) || ($it->{"vpn_satm$number"} > 28800)) {
		return "satmerror";
	}

	if ($it->{"vpn_keytm$number"} < $it->{"vpn_satm$number"}){
		return "keylssaerror";
	}

	if ($it->{"vpn_satm$number"} < ($it->{"vpn_keymg$number"} * 2)){
		return "salskeymgerror";
	}

	#dpddelay
	if (&hyper::checknumstring($it->{"vpn_dpddelay$number"}) == 0) {
		return "dpddelayerror";
	}
	if (($it->{"vpn_dpddelay$number"} < 5) || ($it->{"vpn_dpddelay$number"} > 86400)) {
		return "dpddelayerror";
	}

	#dpdtmout
	if (&hyper::checknumstring($it->{"vpn_dpdtmout$number"}) == 0) {
		return "dpdtmerror";
	}
	if (($it->{"vpn_dpdtmout$number"} < 5) || ($it->{"vpn_dpdtmout$number"} > 86400)) {
		return "dpdtmerror";
	}

	return undef;
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
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0>$va_pr0 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1>$va_pr1 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value2\" $checked2>$va_pr2 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value3\" $checked3>$va_pr3";
	
	return $p;
}

sub set_radio5_pr{
	my ($name,$v,$value0,$value1,$value2,$value3,$value4,$va_pr0,$va_pr1,$va_pr2,$va_pr3,$va_pr4) = @_;
	my $p = "";
	my $checked0 = "";
	my $checked1 = "";
	my $checked2 = "";
	my $checked3 = "";
	my $checked4 = "";

	if("$v" eq "$value0"){
		$checked0 = "checked";
	}elsif("$v" eq "$value1"){
		$checked1 = "checked";
	}elsif("$v" eq "$value2"){
		$checked2 = "checked";
	}elsif("$v" eq "$value3"){
		$checked3 = "checked";
	}else{
		$checked4 = "checked";
	}
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0>$va_pr0 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1>$va_pr1 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value2\" $checked2>$va_pr2 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value3\" $checked3>$va_pr3";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value4\" $checked4>$va_pr4";

	return $p;
}

sub set_checkbox_pr {
	my ($n,$v,$value0,$va_pr0,$en) = @_;
	my $p = "";
	my $checked = "";

	if("$v" eq "$value0"){
		$checked = "checked";
	}else{
		$checked = "";
	}

	$p = "<INPUT type=\"checkbox\" name=\"$n\" value=\"$value0\"  $checked $en>$va_pr0";

	return $p;
}

sub set_input_pr{
	my ($n,$v,$s,$l,$en,$u) = @_;
	my $p = "";

	$p = "<INPUT size=\"$s\" type=\"text\" maxlength=\"$l\" name=\"$n\" value=\"$v\" $en>";
	$p = $p."��$u";

	return $p;
}


my $inputvpn_name = &set_input_pr("vpn_name$number", $items{"vpn_name$number"}, "31", "16","","");
my $inputvpn_use = &set_radio_pr("vpn_use$number", $items{"vpn_use$number"}, "0", "1", "̵��", "ͭ��");
my $inputvpn_mode = &set_radio_pr("vpn_mode$number", $items{"vpn_mode$number"}, "main", "aggr", "�ᥤ��⡼��", "������å��֥⡼��");
my $inputvpn_type = &set_radio_pr("vpn_type$number", $items{"vpn_type$number"}, "tunnel", "transport", "�ȥ�ͥ�", "�ȥ�󥹥ݡ���");
my $inputvpn_ladsel = &set_radio_pr("vpn_ladsel$number", $items{"vpn_ladsel$number"}, "0", "1", "�ǥե����", "IP����");
my $inputvpn_lad = &set_input_pr("vpn_lad$number", $items{"vpn_lad$number"}, "31", "15","","");
my $inputvpn_lsubsel = &set_radio_pr("vpn_lsubsel$number", $items{"vpn_lsubsel$number"}, "0", "1", "���Ѥ��ʤ�", "���Ѥ���");
my $inputvpn_lsub = &set_input_pr("vpn_lsub$number", $items{"vpn_lsub$number"}, "40", "31","","");
my $inputvpn_lid = &set_input_pr("vpn_lid$number", $items{"vpn_lid$number"}, "31", "16","","");
my $inputvpn_lhopsel = &set_radio3_pr("vpn_lhopsel$number", $items{"vpn_lhopsel$number"}, "0", "1", "2", "�ǥե����","IP����", "�ʤ�");
my $inputvpn_lhop = &set_input_pr("vpn_lhop$number", $items{"vpn_lhop$number"}, "31", "16","","");
my $inputvpn_radsel = &set_radio3_pr("vpn_radsel$number", $items{"vpn_radsel$number"}, "0", "1", "2",  "ANY", "IP����", "�ɥᥤ��̾����");
my $inputvpn_rad = &set_input_pr("vpn_rad$number", $items{"vpn_rad$number"}, "40", "64","","");
my $inputvpn_rsubsel = &set_radio_pr("vpn_rsubsel$number", $items{"vpn_rsubsel$number"}, "0", "1", "���Ѥ��ʤ�", "���Ѥ���");
my $inputvpn_rsub = &set_input_pr("vpn_rsub$number", $items{"vpn_rsub$number"}, "40", "31","","");
my $inputvpn_rid = &set_input_pr("vpn_rid$number", $items{"vpn_rid$number"}, "31", "16","","");
my $inputvpn_keysel = &set_radio_pr("vpn_keysel$number", $items{"vpn_keysel$number"}, "secret", "rsasig", "��ͭ������(PSK)", "����������(RSA)");
my $inputvpn_psk = &set_input_pr("vpn_psk$number", $items{"vpn_psk$number"}, "60", "32","","");
my $inputvpn_rsa = &set_input_pr("vpn_rsa$number", $items{"vpn_rsa$number"}, "31", "1024","","");
my $inputvpn_ikesel = &set_radio5_pr("vpn_ikesel$number", $items{"vpn_ikesel$number"}, "0", "1", "2", "3", "4", "�ǥե����", "3DES-SHA1-MODP1024", "3DES-MD5-MODP1024", "����¾", "�Ի���");
my $inputvpn_ike = &set_input_pr("vpn_ike$number", $items{"vpn_ike$number"}, "60", "32","","");
my $inputvpn_espsel = &set_radio4_pr("vpn_espsel$number", $items{"vpn_espsel$number"}, "0", "1", "2", "3",  "�ǥե����", "3DES-SHA1", "3DES-MD5", "����¾");
my $inputvpn_esp = &set_input_pr("vpn_esp$number", $items{"vpn_esp$number"}, "60", "32","","");
if ($items{"vpn_pfs$number"} eq "no") {$items{"vpn_pfs$number"} = "";}
my $inputvpn_pfs = &set_checkbox_pr("vpn_pfs$number", $items{"vpn_pfs$number"},  "yes", "PFS", "");
my $inputvpn_keymg = &set_input_pr("vpn_keymg$number", $items{"vpn_keymg$number"}, "20", "4","","��");
my $inputvpn_keytm = &set_input_pr("vpn_keytm$number", $items{"vpn_keytm$number"}, "20", "5","","��");
my $inputvpn_satm = &set_input_pr("vpn_satm$number", $items{"vpn_satm$number"}, "20", "5","","��");
my $inputvpn_dpd = &set_radio_pr("vpn_dpd$number", $items{"vpn_dpd$number"}, "0", "1", "̵��", "ͭ��");
my $inputvpn_dpddelay = &set_input_pr("vpn_dpddelay$number", $items{"vpn_dpddelay$number"}, "20", "5","","��");
my $inputvpn_dpdtmout = &set_input_pr("vpn_dpdtmout$number", $items{"vpn_dpdtmout$number"}, "20", "5","","��");
my $inputvpn_dpdact = &set_radio3_pr("vpn_dpdact$number", $items{"vpn_dpdact$number"}, "hold", "clear", "restart_by_peer", "�ݻ�", "����", "����³");
my $inputvpn_auto = &set_radio3_pr("vpn_auto$number", $items{"vpn_auto$number"}, "start", "add", "route", "����", "�Ե�", "-");
my $inputvpn_rekey = &set_radio_pr("vpn_rekey$number", $items{"vpn_rekey$number"}, "no", "yes", "�ʤ�", "����");

my $tb1_w1 ="width=\"140\"";
my $tb1_w2 ="width=\"240\"";
my $tb1_w3 ="width=\"220\"";


print "Content-Type:text/html\r\n\r\n";
print <<"EOFHTML";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 10.0.2.0 for Windows">
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
<TITLE></TITLE>
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
$err_item
<H2>��³$number</H2>
<FORM method="POST" action="./vpnsetup.cgi">
<INPUT type="submit" name="btnSet" value="����¸">��<INPUT type="submit" name="btnRetry" value="���ľ��">
<INPUT type="hidden" name="number" value="$number">
<TABLE border="0">
  <TBODY>
    <TR>
      <TD>
      <TABLE border="1">
        <TBODY>
          <TR>
            <TD $tb1_w1>̾��(name|use)</TD>
           <TD $tb1_w2 >$inputvpn_name</TD>
           <TD $tb1_w3 >$inputvpn_use</TD>
          </TR>
          <TR>
            <TD>�⡼��(mode)</TD>
           <TD colspan="2">$inputvpn_mode</TD>
          </TR>
<!--
          <TR>
            <TD>������(type)</TD>
           <TD colspan="2">$inputvpn_type</TD>
          </TR>
-->
          <TR>
            <TD>������</TD>
            <TD colspan="2">��</TD>
          </TR>
          <TR>
            <TD>�����ɥ쥹(ladsel|lad)</TD>
            <TD>$inputvpn_ladsel</TD>
           <TD>$inputvpn_lad</TD>
          </TR>
          <TR>
            <TD>�����֥ͥåȥ��ɥ쥹(lsubsel|lsub)</TD>
            <TD>$inputvpn_lsubsel</TD>
           <TD>$inputvpn_lsub</TD>
          </TR>
          <TR>
            <TD>��ID(lid)</TD>
           <TD colspan="2"> $inputvpn_lid</TD>
          </TR>
          <TR>
            <TD>���ͥ����ȥۥå�(lhopsel|lhop)</TD>
            <TD>$inputvpn_lhopsel</TD>
           <TD>$inputvpn_lhop</TD>
          </TR>
          <TR>
            <TD>��⡼��</TD>
            <TD colspan="2">��</TD>
          </TR>
          <TR>
            <TD>�����ɥ쥹(radsel|rad)</TD>
            <TD>$inputvpn_radsel</TD>
           <TD>$inputvpn_rad</TD>
          </TR>
          <TR>
            <TD>�����֥ͥåȥ��ɥ쥹(rsubsel|rsub)</TD>
            <TD>$inputvpn_rsubsel</TD>
           <TD>$inputvpn_rsub</TD>
          </TR>
          <TR>
            <TD>��ID(rid)</TD>
           <TD colspan="2">$inputvpn_rid</TD>
          </TR>
          <TR>
            <TD>ǧ�ڸ�(keysel)</TD>
            <TD colspan="2">$inputvpn_keysel</TD>
          </TR>
          <TR>
            <TD>����ͭ��(psk)</TD>
            <TD colspan="2">$inputvpn_psk</TD>
          </TR>
          <TR>
            <TD>����⡼�ȸ�����(rsa)</TD>
            <TD colspan="2"><textarea name="vpn_rsa$number" cols="55" rows="5" wrap="soft" >$items{"vpn_rsa$number"}</textarea></TD>
          </TR>
          <TR>
            <TD>�Ź�����</TD>
            <TD colspan="2">��</TD>
          </TR>
            <TD>���ե�����1(ikesel)</TD>
            <TD colspan="2">$inputvpn_ikesel</TD>
          </TR>
          </TR>
            <TD colspan="1">��(ike)</TD>
            <TD colspan="2">$inputvpn_ike</TD>
          </TR>
          </TR>
            <TD>���ե�����2(espsel)</TD>
            <TD colspan="2">$inputvpn_espsel</TD>
          </TR>
          </TR>
            <TD colspan="1">��(esp)</TD>
            <TD colspan="2">$inputvpn_esp</TD>
          </TR>
          <TR>
            <TD>���ץ����</TD>
            <TD colspan="2">��</TD>
          </TR>
          <TD colspan="1">��(pfs)</TD>
            <TD colspan="2">$inputvpn_pfs</TD>
          </TR>
          <TR>
          <TD colspan="1">��</TD>
            <TD>���򴹤Υޡ�����(keymg)</TD>
            <TD>$inputvpn_keymg</TD>
          </TR>
          <TR>
          <TD colspan="1">��</TD>
            <TD>���μ�̿(keytm)</TD>
            <TD>$inputvpn_keytm</TD>
          </TR>
          <TR>
          <TD colspan="1">��</TD>
            <TD>SA�μ�̿(satm)</TD>
            <TD>$inputvpn_satm</TD>
          </TR>
          <TR>
            <TD>DeadPeerDetection(dpd)</TD>
           <TD colspan="2">$inputvpn_dpd</TD>
          </TR>
          <TR>
          <TD colspan="1">��</TD>
            <TD>DPD�����ֳ�(dpddelay)</TD>
            <TD>$inputvpn_dpddelay</TD>
          </TR>
          <TR>
          <TD colspan="1">��</TD>
            <TD>DPD�����ॢ����(dpdtmout)</TD>
            <TD>$inputvpn_dpdtmout</TD>
          </TR>
          <TR>
          <TD colspan="1">��</TD>
            <TD>DPD���������(dpdact)</TD>
           <TD colspan="2">$inputvpn_dpdact</TD>
          </TR>
          <TR>
            <TD>��³��ˡ(auto)</TD>
            <TD colspan="2">$inputvpn_auto</TD>
          <TR>
          <TR>
            <TD>�ꥭ��(rekey)</TD>
            <TD colspan="2">$inputvpn_rekey</TD>
          <TR>
        </TBODY>
      </TABLE>
     </TD>
</TABLE>
<BR>
����ե�����
<BR>
<INPUT type="submit" name="btnRead" value="�ɽФ�">
<BR>
</FORM>
<form action="./vpnload.cgi" enctype="multipart/form-data" method="post">
<input name="confFile" type="file" size="50" accept="application/octet-stream">
<INPUT type="hidden" name="number" value="$number">
<BR>
<INPUT type="submit" name="btnWrite" value="�����">
</FORM> 
</BODY>
</HTML>
EOFHTML
