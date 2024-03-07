#!/usr/bin/perl -w
#use CGI::Carp qw(fatalsToBrowser);
#use strict;
#use warnings;

require "/home/httpd/cgi-bin/hyper.pl";

#-------------------
# �����˥塼ɽ��
#-------------------

my $commandline = "";
my $login_user = "";
my $contents = "";

sub HtmlTopJs{
  return <<END_OF_TEXT;
<!DOCTYPE HTML>
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE></TITLE>
<LINK href="./../html/status.css" rel="stylesheet" type="text/css">
<script type="text/javascript">
<!--
function showPlagin(idno){
    pc = ('PlagClose' + (idno));
    po = ('PlagOpen' + (idno));
    if( document.getElementById(pc).style.display == "none" ){
        document.getElementById(pc).style.display = "block";
        document.getElementById(po).style.display = "none";
    }else{
        document.getElementById(pc).style.display = "none";
        document.getElementById(po).style.display = "block";
    }
}
-->
</script>
</HEAD>
END_OF_TEXT
}

#BODY_TOP
sub HtmlBody{
  return <<END_OF_TEXT;
<BODY>
<CENTER>
END_OF_TEXT
}

#BOTTOM
sub HtmlBottom{
  return <<END_OF_TEXT;
</CENTER>
</BODY>
</HTML>
END_OF_TEXT
}

#LINK
sub HtmlLink{
  my($name, $href) = @_; # name:����̾��, href:URL
  return <<END_OF_TEXT;
<TR><TD width="220"><FONT color="#0000ff"><A href="$href" target="right">$name</A></FONT></TD></TR>
END_OF_TEXT
}

#�ޤꤿ����
sub HtmlFold{
  my ($id,$name,$contents) = @_;
  my $outtag = "";
$outtag = '<div id="PlagOpen'.$id.'">';
$outtag .= '<p></p>';
$outtag .= '<TABLE>';
$outtag .= '<tr><th width="220px"><a href="#" onclick="showPlagin('.$id.');return false;">'.$name.'��</a></th></tr>';
$outtag .= '</TABLE>';
$outtag .= '</div>';

$outtag .= '<div id="PlagClose'.$id.'" style="display: none">';
$outtag .= '<p></p>';
$outtag .= '<TABLE>';
$outtag .= '<tr><th width="220px"><a href="#" onclick="showPlagin('.$id.');return false;">'.$name.'��</a></th></tr>';
$outtag .= $contents;
$outtag .= '</TABLE>';
$outtag .= '</div>';
return $outtag;
}

print "Content-Type:text/html\r\n\r\n";
print &HtmlTopJs;
$login_user = &hyper::get_logincheck();

print &HtmlBody;

# ��������
$contents = &HtmlLink("��������","general.cgi");
$contents .= &HtmlLink("�ͥåȥ��","network.cgi");
$contents .= &HtmlLink("WAN����","wansetup.cgi");
#$contents .= &HtmlLink("SMS�忮����","smssetup.cgi");
print &HtmlFold(1,"��������", $contents);

# NAT���������ƥ�
$contents = &HtmlLink("��ŪNAT����","snatsetup.cgi");
$contents .= &HtmlLink("VPN����","vpn.cgi");
$contents .= &HtmlLink("�ե��륿����","filterview.cgi");
print &HtmlFold(2,"NAT���������ƥ�", $contents);

# �롼����ǽ
$contents = &HtmlLink("�����ʥߥå�DNS","ddnssetup.cgi");
$contents .= &HtmlLink("DHCP����","dhcpsetup.cgi");
$contents .= &HtmlLink("NTP����","ntpsetup.cgi");
print &HtmlFold(3,"�롼����ǽ", $contents);

# RS232C�ץ���
$contents = &HtmlLink("RS-232C�ץ�ȥ����Ѵ�","rssetup.cgi");
$contents .= &HtmlLink("��å�����&������","rsstatussetup.cgi");
print &HtmlFold(4,"�ץ�ȥ����Ѵ�", $contents);

# ����¾��ǽ
$contents = &HtmlLink("����¾����","etcsetup.cgi");
$contents .= &HtmlLink("����¾���ꣲ","etcsetup2.cgi");
print &HtmlFold(5,"����¾��ǽ", $contents);

# IOT
$contents = &HtmlLink("MQTT�ѥ֥�å��㡼","mqttpubsetup.cgi");
$contents .= &HtmlLink("��������","mqttsendsetup.cgi");
$contents .= &HtmlLink("CAǧ�ڶ�","cacrtfile.cgi");
$contents .= &HtmlLink("���饤����Ⱦ�����","clicrtfile.cgi");
$contents .= &HtmlLink("���饤�������̩��","privatefile.cgi");
#$contents .= &HtmlLink("MQTT�֥�����","mqttbrsetup.cgi");
print &HtmlFold(6,"IOT", $contents);

# ������¸
$contents = &HtmlLink("������¸","setup.cgi");
$contents .= &HtmlLink("�����","init.cgi");
$contents .= &HtmlLink("������ե�����","configfile.cgi");
print &HtmlFold(7,"������¸", $contents);

# ���ƥʥ�
$contents = &HtmlLink("ư���","log_get.cgi");
$contents .= &HtmlLink("�ѥ�����ѹ�","password.cgi");
$contents .= &HtmlLink("�Ƶ�ư","restart.cgi");
#$contents .= &HtmlLink("�⥸�塼�빹��","fota.cgi");
$contents .= &HtmlLink("�С�����󥢥å�","versionup.cgi");
print &HtmlFold(8,"���ƥʥ�", $contents);

print '<P><A href="http://www.i-netd.co.jp/" target="_parent"><IMG src="../img/logo2.jpg" width="139" height="23" border="0" align="middle" alt="������� iND"></A></P>';

print &HtmlBottom;
