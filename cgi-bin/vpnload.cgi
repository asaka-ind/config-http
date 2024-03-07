#!/usr/bin/perl -w
###! /usr/local/bin/perl

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/vpn.pl";

%FORM = (
 'number'      => "0",
 'btnWrite'     => "",
 'confFile'      => "",
);

%error_list = (
 '1'  => '�ե��������ꤷ�Ƥ���������',
 '2'  => '�ե����륵�������礭�᤮�ޤ���',
 '3'  => '�ե�����Υ����פ��㤤�ޤ���',
 '4'  => '���åץǡ��Ⱦ���(����)�˸�꤬����ޤ���',
 '5'  => '���ߤΥС��������Ť��С���������ꤷ�ޤ�����',
 '99' => 'ͽ�����̥��顼��ȯ�����ޤ�����',
 'nameerror'      => "��³̾��(nam)�ϱѿ���16ʸ����������ꤷ�Ƥ���������",
 'useerror'      => "��³ͭ����̵��(use)��[0:̵����1:ͭ��]�����ꤷ�Ƥ���������",
 'typeerror'      => "������(type)��[tunnel��transport]�����ꤷ�Ƥ���������",
 'ladselerror'      => "�����륢�ɥ쥹����(ladsel)��[0:�ǥե���ȡ�1:IP����]�����ꤷ�Ƥ���������",
 'ladiperror'      => "�����륢�ɥ쥹(lad)�����꤬����������ޤ��󡣡��㡧192.168.10.100)",
 'lsubselerror'      => "�����륵�֥ͥåȥ��ɥ쥹����(lsubsel)��[0:���Ѥ��ʤ���1:���Ѥ���]�����ꤷ�Ƥ���������",
 'lsuberror'      => "�����륵�֥ͥåȥ��ɥ쥹(lsub)�����꤬����������ޤ��󡣡��㡧192.168.10.100/24 �ޤ��� 192.168.10.100/255.255.255.0��",
 'liderror'      => "������ID(lid)�ϱѿ���16ʸ����������ꤷ�Ƥ���������",
 'lhopselerror'      => "������ͥ����ȥۥå�����(lhopsel)��[0:�ǥե���ȡ�1:IP���ꡢ2:�ʤ�]�����ꤷ�Ƥ���������",
 'lhoperror'      => "������ͥ���ȥۥåץ��ɥ쥹(lhop)�����꤬����������ޤ��󡣡��㡧192.168.10.100)",
 'radselerror'      => "��⡼�ȥ��ɥ쥹����(radsel)��[0:any��1:IP���ꡢ2:�ɥᥤ��̾����]�����ꤷ�Ƥ���������",
 'raderror'      => "��⡼�ȥ��ɥ쥹(rad)�ϱѿ���64ʸ����������ꤷ�Ƥ���������",
 'rsubselerror'      => "��⡼�ȥ��֥ͥåȥ��ɥ쥹����(rsubsel)��[0:���Ѥ��ʤ���1:���Ѥ���]�����ꤷ�Ƥ���������",
 'rsuberror'      => "��⡼�ȥ��֥ͥåȥ��ɥ쥹(rsub)�����꤬����������ޤ��󡣡��㡧192.168.10.100/24 �ޤ��� 192.168.10.100/255.255.255.0��",
 'riderror'      => "��⡼��ID(rid)�ϱѿ���16ʸ����������ꤷ�Ƥ���������",
 'keyselerror'      => "ǧ�ڸ�(keysek)��[secret:��ͭ��������rsasig:����������]�����ꤷ�Ƥ���������",
 'pskerror'      => "��ͭ��(psk)�ϱѿ���32ʸ����������ꤷ�Ƥ���������",
 'rsaerror'      => "��ͭ��(rsa)���ͤ������ͤǤ���",
 'ikeselerror'      => "�Ź������ե�����1����(ikesel)��[0:�ǥե���ȡ�1:3DES-SHA1-MODP1024��2:3DES-MD5-MODP1024��3:����¾��4:�Ի���]�����ꤷ�Ƥ���������",
 'ikeerror'      => "�Ź������ե�����1(ike)�����꤬����������ޤ���",
 'espselerror'      => "�Ź������ե�����2����(espsel)��[0:�ǥե���ȡ�1:3DES-SHA1��2:3DES-MD5��3:����¾]�����ꤷ�Ƥ���������",
 'esperror'      => "�Ź������ե�����2(esp)�����꤬����������ޤ���",
 'pfserror'      => "PFS(pfs)��[no:�����å��ʤ���yes:�����å�����]�����ꤷ�Ƥ���������",
 'keymgerror'      => "���򴹤Υޡ�����(keymg)��30��3600�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'keytmerror'      => "���μ�̿(keytm)��0��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'satmerror'      => "SA�μ�̿(satm)��0��28800�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'dpderror'      => "DeadPeerDetection(dpd)��[0:̵����1:ͭ��]�����ꤷ�Ƥ���������",
 'dpdacterror'      => "DPD���������(dpdact)��[hold:�ݻ���clear:���ǡ�restart_by_peer:����³]�����ꤷ�Ƥ���������",
 'dpddelayerror'      => "DPD�����ֳ֤�5��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'dpdtmerror'      => "DPD�����ॢ���Ȥ�5��86400�ä��ϰϤǻ��ꤷ�Ƥ���������",
 'autoerror'      => "��³��ˡ(auto)��[start:���ϡ�add:�Ե���route:���٥��]�����ꤷ�Ƥ���������",
 'rekeyerror'      => "�ꥭ��(rekey)��[no:�ʤ���yes:����]�����ꤷ�Ƥ���������",
);

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

# �������ޥ����ѥ�᡼��
#$upload_dir = "../../../var";  # ���åץ��ɥե�������Ǽ����ǥ��쥯�ȥ�

# ɸ�����Ϥ���ǡ������ɤߤ���
$buf = "";
$read_data = "";
#$commandline = "";
$number = 0;
$Writefile = "";
$ConfFile = "";

$remain = $ENV{'CONTENT_LENGTH'};
binmode(STDIN);
while ($remain) {
  $len = sysread(STDIN, $buf, $remain);
  if (!$len) {
    last;
  }
  $remain -= $len;
  $read_data .= $buf;
}


=pod
$commandline = $read_data;
if ( ! defined $commandline) {
#�������ʤ��Ȥ��Ͻ�λ
	print "Location: ./general.cgi\n\n";
}

$commandline = hyper::url_decode($commandline);
$number = &hyper::get_param("number", $commandline);
$Writefile = &hyper::get_param("btnWrite", $commandline);
$ConfFile = &hyper::get_param("confFile", $commandline);
=cut
# �ǡ������᤹��
$pos1 = 0; # �إå�������Ƭ
$pos2 = 0; # �ܥǥ�������Ƭ
$pos3 = 0; # �ܥǥ����ν�ü
$delimiter = "";
$max_count = 0;
$ret = "";
$tmp_file = &vpn::get_conf_file();
#�ե��������
 	unlink "$tmp_file";

while (1) {

	# �إå�����
	$pos2 = index($read_data, "\r\n\r\n", $pos1) + 4;
	my @headers = split("\r\n", substr($read_data, $pos1, $pos2 - $pos1));
	$filename = "";
	$name = "";
	foreach (@headers) {
		if ($delimiter eq "") {
			$delimiter = $_;
		} elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"/i) {
			if ($3) {
				$filename = $3;
				if ($filename =~ /([^\\\/]+)$/) {
					$filename = $1;
				}
			}
		} elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"/i) {
			$name = $2;
		}
	}

	# �ܥǥ�����
	$pos3 = index($read_data, "\r\n$delimiter", $pos2);
	$size = $pos3 - $pos2;
	if ($filename) {
		if ($size < 2048){
		 	if (open(OUT, "> $tmp_file")) {
				binmode(OUT);
				print OUT substr($read_data, $pos2, $size);
				close(OUT);
			}
			$FORM{"confFile"} = $filename;
		}else{
			$ret = "2";
		}
	} elsif ($name) {
		$FORM{$name} = substr($read_data, $pos2, $size);
	}

	# ��λ����
	$pos1 = $pos3 + length("\r\n$delimiter");
	if (substr($read_data, $pos1, 4) eq "--\r\n") {
		# ���٤ƤΥե�����ν�ü
		 last;
	} else {
		# ���Υե�������ɤ߽Ф�
		$pos1 += 2;
		if ($max_count++ > 16) { last; }
		next;
	}
}

$number = $FORM{"number"};
$Writefile = $FORM{"btnWrite"};
$ConfFile = $FORM{"confFile"};
#print "Location:./general.cgi\n\n";
#my $ret = `/opt/sbin/chk_verup`;

if ($ret eq "" && $ConfFile eq ""){
	$ret = "1";
}elsif ($ret ne "2"){
	$ret = chk_vpnfile($tmp_file);
}


sub chk_vpnfile{
	my $filename = $_[0];
	my $ret = "3";
	my %hashs = ();

	%hashs = &hyper::readfile_hash($filename);

	my @Key = &vpn::get_item_vpnsetn();
	foreach my $keyn (@Key) {
		if ( exists $hashs{"$keyn"}){
			$ret = "";
		}
	}

	if($ret eq ""){
		$ret = &chk_vpndata(\%hashs);
	}
	return $ret;
}

sub chk_radio{
	my ($v,@dt) = @_;
	my $ret = 0;

	foreach my $dt (@dt) {
		if ($v eq $dt){
			$ret = 1;
			last;
		}
	}
	return $ret;
}

sub chk_vpndata{
	my $it = $_[0];
	my $ret = 0;
	#name
	if (defined $it->{"name"}) {
		if (&hyper::chk_graph($it->{"name"}, 16) eq "" ) {
			return "nameerror";
		}
	}
	#use
	if (exists $it->{"use"}) {
		$ret = &chk_radio($it->{"use"},"0","1");
		if ($ret == 0) {
			return "useerror";
		}
	}
	#type
	if (exists $it->{"type"}) {
		$ret = &chk_radio($it->{"type"},"tunnel","transport");
		if ($ret == 0) {
			return "typeerror";
		}
	}
	#lad
	if (exists $it->{"ladsel"}) {
		$ret = &chk_radio($it->{"ladsel"},"0","1");
		if ($ret == 0) {
			return "ladselerror";
		}
	}
	if (exists $it->{"lad"}) {
		if ((length $it->{"lad"}) && (&hyper::get_ipaddress($it->{"lad"}, 1) eq "")) {
			return "ladiperror";
		}
	}
	#lsub
	if (exists $it->{"lsubsel"}) {
		$ret = &chk_radio($it->{"lsubsel"},"0","1");
		if ($ret == 0) {
			return "lsubselerror";
		}
	}
	if (exists $it->{"lsub"}) {
		if ((length $it->{"lsub"}) && (&vpn::get_subnetaddress($it->{"lsub"}, 1) eq "")) {
			return "lsuberror";
		}
	}
	#lid
	if (exists $it->{"lid"}) {
		if (&hyper::chk_graph($it->{"lid"}, 16) eq "" ) {
			return "liderror";
		}
	}
	#lhop
	if (exists $it->{"lhopsel"}) {
		$ret = &chk_radio($it->{"lhopsel"},"0","1","2");
		if ($ret == 0) {
			return "lhopselerror";
		}
	}
	if (exists $it->{"lhop"}) {
		if ((length $it->{"lhop"}) && (&hyper::get_ipaddress($it->{"lhop"}, 1) eq "")) {
			return "lhoperror";
		}
	}
	#rad
	if (exists $it->{"radsel"}) {
		$ret = &chk_radio($it->{"radsel"},"0","1","2");
		if ($ret == 0) {
			return "radselerror";
		}
	}
	if (exists $it->{"rad"}) {
		if  (&hyper::chk_graph($it->{"rad"}, 64) eq "" ) {
			return "raderror";
		}
	}
	#rsub
	if (exists $it->{"rsubsel"}) {
		$ret = &chk_radio($it->{"rsubsel"},"0","1");
		if ($ret == 0) {
			return "rsubselerror";
		}
	}
	if (exists $it->{"rsub"}) {
		if ((length $it->{"rsub"}) && (&vpn::get_subnetaddress($it->{"rsub"}, 1) eq "")) {
			return "rsuberror";
		}
	}
	#rid
	if (exists $it->{"rid"}) {
		if (&hyper::chk_graph($it->{"rid"}, 16) eq "" ) {
			return "riderror";
		}
	}
	#keysel
	if (exists $it->{"keysel"}) {
		$ret = &chk_radio($it->{"keysel"},"secret","rsasig");
		if ($ret == 0) {
			return "keyselerror";
		}
	}
	#psk
	if (exists $it->{"psk"}) {
		if (&hyper::chk_graph($it->{"psk"}, 32) eq "" ) {
			return "pskerror";
		}
	}
	#rsa
	if (exists $it->{"rsa"}) {
		if (&hyper::chk_graph($it->{"rsa"}, 600) eq "" ) {
			return "rsaerror";
		}
	}
	#ike
	if (exists $it->{"ikesel"}) {
		$ret = &chk_radio($it->{"ikesel"},"0","1","2","3","4");
		if ($ret == 0) {
			return "ikeselerror";
		}
	}
	if (exists $it->{"ike"}) {
		if ((length $it->{"ike"}) && (&hyper::chk_graph($it->{"ike"}, 32) eq "" )) {
			return "ikeerror";
		}
	}
	#esp
	if (exists $it->{"espsel"}) {
		$ret = &chk_radio($it->{"espsel"},"0","1","2","3");
		if ($ret == 0) {
			return "espselerror";
		}
	}
	if (exists $it->{"esp"}) {
		if ((length $it->{"esp"}) && (&hyper::chk_graph($it->{"esp"}, 32) eq "" )) {
			return "esperror";
		}
	}
	#pfs
	if (exists $it->{"pfs"}) {
		$ret = &chk_radio($it->{"pfs"},"no","yes");
		if ($ret == 0) {
			return "pfserror";
		}
	}
	#kyemg
	if (exists $it->{"keymg"}) {
		if (&hyper::checknumstring($it->{"keymg"}) == 0) {
			return "keymgerror";
		}
		if (($it->{"keymg"} < 30) || ($it->{"keymg"} > 3600)) {
			return "keymgerror";
		}
	}
	#kyetm
	if (exists $it->{"keytm"}) {
		if (&hyper::checknumstring($it->{"keytm"}) == 0) {
			return "keytmerror";
		}
		if (($it->{"keytm"} < 0) || ($it->{"keytm"} > 86400)) {
			return "keytmerror";
		}
	}
	#satm
	if (exists $it->{"satm"}) {
		if (&hyper::checknumstring($it->{"satm"}) == 0) {
			return "satmerror";
		}
		if (($it->{"satm"} < 0) || ($it->{"satm"} > 28800)) {
			return "satmerror";
		}
	}
	#dpd
	if (exists $it->{"dpd"}) {
		$ret = &chk_radio($it->{"dpd"},"0","1");
		if ($ret == 0) {
			return "dpderror";
		}
	}
	#dpdact
	if (exists $it->{"dpdact"}) {
		$ret = &chk_radio($it->{"dpdact"},"hold","clear","restart_by_peer");
		if ($ret == 0) {
			return "dpdacterror";
		}
	}
	#dpdtmout
	if (exists $it->{"dpdtmout"}) {
		if (&hyper::checknumstring($it->{"dpdtmout"}) == 0) {
			return "dpdtmerror";
		}
		if (($it->{"dpdtmout"} < 5) || ($it->{"dpdtmout"} > 86400)) {
			return "dpdtmerror";
		}
	}
	#dpddelay
	if (exists $it->{"dpddelay"}) {
		if (&hyper::checknumstring($it->{"dpddelay"}) == 0) {
			return "dpddelayerror";
		}
		if (($it->{"dpddelay"} < 5) || ($it->{"dpddelay"} > 86400)) {
			return "dpddelayerror";
		}
	}
	#auto
	if (exists $it->{"auto"}) {
		$ret = &chk_radio($it->{"auto"},"start","add","route");
		if ($ret == 0) {
			return "autoerror";
		}
	}
	#rekey
	if (exists $it->{"rekey"}) {
		$ret = &chk_radio($it->{"rekey"},"no","yes");
		if ($ret == 0) {
			return "rekeyerror";
		}
	}
	return undef;

}

if ($ret ne "") {

#�ե��������
 	unlink "$tmp_file";

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
</HEAD>
<BODY bgcolor="#cccccc">
<H2 align="center">����ե���������å�</H2>
<FORM action="./vpnsetup.cgi">
<INPUT type="hidden" name="number" value="$number">
<CENTER>
<P>����ե����뤬����������ޤ���</P>
<P>$error_list{$ret}</P>
<P/>
<P><INPUT type="submit" name="btnReset" value="���"></P>
</CENTER>
</FORM>
</BODY>
</HTML>
EOFHTML

}
else {
=pod
#print "FILENAME = $filename\n";
 #if ($filename ne "") {
	$filename = "$upload_dir/$filename";
#print "FILENAME = $filename\n";
	my %hashs = ();
	%hashs = &hyper::readfile_hash($filename);
#print "hashs = $hashs{name}\n";
#print $hashs;
#	my @Key = @vpn::item_vpnsetn;
	my @Key = ();
#	&vpn::get_item_vpnsetn(\@Key);
	@Key = &vpn::get_item_vpnsetn();
	my $number = "1";
	my $pr = "number=$number";	
#	foreach my $keyn (@Key) {
	foreach my $keyn (@Key) {
		my $p = "vpn_$keyn$number=$hashs{\"$keyn\"}";
		$pr = $pr."&".$p;
    }
=cut
print "Content-Type:text/html\r\n\r\n";
print <<EOFRESTART;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<STYLE TYPE="text/css">
</STYLE>
<SCRIPT Language="JavaScript">
<!--

//����ư������
function autoLink()
{
	location.href = "./vpnsetup.cgi?number=$number&btnWrite=1";
}
// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="autoLink();">
<H2 align="center">�����ͥ빹��</H2>
<FORM action="./vpnsetup.cgi">
<INPUT type="hidden" name="number" value="1">

</FORM>
</BODY>
</HTML>
EOFRESTART
}

