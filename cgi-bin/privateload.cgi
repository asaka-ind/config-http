#!/usr/bin/perl -w
###! /usr/local/bin/perl

require "hyper.pl";

%FORM = (
 'number'      => "0",
 'btnWrite'     => "",
 'confFile'      => "",
);

%error_list = (
 '1'  => '�ե��������ꤷ�Ƥ���������',
 '2'  => '�ե����륵�������礭�᤮�ޤ���',
 '3'  => '�ե�����Υ����פ��㤤�ޤ���(private.key)',
 '4'  => '���åץǡ��Ⱦ���(����)�˸�꤬����ޤ���',
 '5'  => '���ߤΥС��������Ť��С���������ꤷ�ޤ�����',
 '99' => 'ͽ�����̥��顼��ȯ�����ޤ�����',
);

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Location: ./general.cgi\n\n";
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
$tmp_file = "/tmp/private.key.tmp";
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
		if ($filename ne "private.key") {
			$ret = "3";
		}	
		if ($size < 100000){
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
}elsif ($ret ne "2" && $ret ne "3"){
	$ret = "";
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
<H2 align="center">�ե���������å�</H2>
<FORM action="./privatefile.cgi">
<INPUT type="hidden" name="number" value="$number">
<CENTER>
<P>�ե����뤬����������ޤ���</P>
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
	location.href = "./privatefile.cgi?&btnWrite=1";
}
// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="autoLink();">
<H2 align="center">�����ͥ빹��</H2>
<FORM action="./privatefile.cgi">
<INPUT type="hidden" name="number" value="1">

</FORM>
</BODY>
</HTML>
EOFRESTART
}

