#!/usr/bin/perl -w
###! /usr/local/bin/perl

require "hyper.pl";

%error_list = (
 '1'  => '�ե����뤬�ɤ߹���ޤ���',
 '2'  => '���åץǡ��Ⱦ���(����������)�˸�꤬����ޤ���',
 '3'  => '���󥹥ȡ��륿���פȰ㤦�����פΥ��åץǡ��ȥե��������ꤷ�ޤ�����',
 '4'  => '���åץǡ��Ȥ˼��Ԥ��ޤ�����',
 '5'  => '���ߤΥС��������Ť��С���������ꤷ�ޤ�����',
 '99' => 'ͽ�����̥��顼��ȯ�����ޤ�����',
);

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
}

# �������ޥ����ѥ�᡼��
$upload_dir = "/mnt/ramdisk";  # ���åץ��ɥե�������Ǽ����ǥ��쥯�ȥ�
$state_file = "dl_file.status"; # download file status
$log_files = "/tmp/log*";

$ret = 0;

# ɸ�����Ϥ���ǡ������ɤߤ���
$buf = "";
$len = 0;
$read_data = "";
$remain = $ENV{'CONTENT_LENGTH'};
$totalsize = 0;
$totalsize = $remain;
binmode(STDIN);
  $len = sysread(STDIN, $buf, 1024);
  die "read error: $filename" unless defined $len;
  if (!$len) {
    $ret = 1;
    goto DONE_STATE;
  }
  $remain -= $len;
  $read_data = $buf;
  $size = $len;
# �ǡ������᤹��
$pos1 = 0; # �إå�������Ƭ
$pos2 = 0; # �ܥǥ�������Ƭ
$pos3 = 0; # �ܥǥ����ν�ü
$delimiter = "";

  # �إå�����
  $pos2 = index($read_data, "\r\n\r\n", $pos1) + 4;
  @headers = split("\r\n", substr($read_data, $pos1, $pos2 - $pos1));
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

  # download file header
  $ps1 = $pos2; # �إå�������Ƭ
  $ps2 = 0; # file name end
  $head_size = 28;
  $filename_d = "";
  $filesize = 0;
  $readlen = 0;
  $ps2 = index($read_data, "\0", $ps1);
  if($ps2 - $ps1 > $head_size){
    $ret = 3;
    goto DONE_STATE;
  }
  $filename_d = substr($read_data, $ps1, $ps2 - $ps1);
#  if($filename_d ne $filename){
#    $ret = 3;
#    goto DONE_STATE;
#  }
  if($filename_d !~ /^HL3\w+.bin/ and $filename_d !~ /^\w+.bin/){
    $ret = 3;
    goto DONE_STATE;
  }
  $filesize = vec(substr($read_data, $ps1 + 24, 4), 0,32);
  if($filesize > $totalsize){
    $ret = 3;
    goto DONE_STATE;
  }
#�ե�������� 090924
 	`rm $upload_dir/*`;
  open(STFILE, "> $upload_dir/$state_file");
      binmode(STFILE);
      print STFILE substr($read_data, $pos2, $head_size);
#      print STFILE sprintf("total size = %lX\n",$totalsize);
#      print STFILE sprintf("dlfile size = %lX\n",$filesize);
  close(STFILE);

  $pos2 += $head_size;

  # �ܥǥ�����
  $pos3 = index($read_data, "\r\n$delimiter", $pos2);
  if($pos3 != -1){
        $size = $pos3 - $pos2;
  }else{
        $size -= $pos2;
  }
  if ($filename_d) {
    if (open(OUT, "> $upload_dir/$filename_d")) {
      binmode(OUT);
      print OUT substr($read_data, $pos2, $size);
    }
  } else {
    $ret = 1;
    goto DONE_STATE;
  }

  $readlen = $filesize - $size;
my $block = 16384;
while ($readlen > $block) {
  $len = sysread(STDIN, $buf, $block);
  die "read error: $filename" unless defined $len;
  last if $len == 0;
  $remain -= $len;
  $readlen -= $len;
   print OUT $buf;
}
while ($readlen) {
  $len = sysread(STDIN, $buf, $readlen);
  die "read error: $filename" unless defined $len;
  last if $len == 0;
  $remain -= $len;
  $readlen -= $len;
   print OUT $buf;
}
while ($remain) {
  $len = sysread(STDIN, $buf, $remain);
  die "read error: $filename" unless defined $len;
  last if $len == 0;
  $remain -= $len;
}
close(OUT);

$size = -s "$upload_dir/$filename_d";
if($size != $filesize){
	$ret = 4;
	goto DONE_STATE
}

DONE_STATE:{

while ($len) {
	$len = sysread(STDIN, $buf, 16384);
  	die "read error: $filename" unless defined $len;
}

if ($ret > 0) {
	if ($ret > 5) {
	# ���顼����̵�����
 		$ret = 99;
	}
#�ե��������
 	unlink "$upload_dir/$filename_d";

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
<H2 align="center">�С�����󥢥å�</H2>
<FORM action="./versionup.cgi">
<CENTER>
<P>�С�����󥢥åץե����뤬����������ޤ���</P>
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
total = 190;			// �ɤ߹���ȡ����������
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

	progTitle.innerText = "���åץǡ��Ƚ�����";
	var kaisu = total-per;
	progMsg.innerText = "��"+kaisu+"�ø�˺���³���Ƥ���������";

	if (per == total) setTimeout("hideProgressBar()",1000);
	else setTimeout('progressBar()',1000);
}
//�����÷вᤷ����ץ��쥹�С���õ�
function hideProgressBar()
{
	progTitle.innerText = "���åץǡ��Ȥ���λ���ޤ�����";
	progMsg.innerText = "LED���ǧ���ƺ���³���Ƥ���������";

	document.all["barBG"].style.visibility = "hidden";
}

// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="progressBar();">
<H2 align="center">�С�����󥢥å�</H2>
<CENTER>
<P><DIV ID="progTitle"></DIV></P>
<P><DIV ID="progMsg"></DIV></P>
</CENTER>
<P><DIV ID="barBG"><DIV ID="bar"></DIV></DIV></P>
</BODY>
</HTML>
EOFRESTART

#my $ret = `/opt/sbin/do_verup &`;

#�ѹ��ե饰��Ω�Ƥ�
	#V104 091019
        `echo 1 > /dev/hl320_module_cnt`;
	`rm $log_files`;
	`sync`;
my $flag = &hyper::get_flag_file($hyper::flag_name{'update'});
my @s = ("1");
&hyper::writefile($flag, @s);

#�Ƶ�ư�ե饰��Ω�Ƥ�
#$flag = &hyper::get_flag_file($hyper::flag_name{'reboot'});
#&hyper::writefile($flag, @s);
}
}
