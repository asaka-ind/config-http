#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

# ���ѥץ�ȥ���
# ������ݡ����ֹ�
# �ץ饤�ޥꥻ�󥿡���IP���ɥ쥹
# ��������ꥻ�󥿡���IP���ɥ쥹
# ��⡼���ڤ��ؤ����
# ��⡼�ȥݡ����ֹ�
# TCP��³��Բ��
# TCP���ǥ����ޡ�
# RS232C���������ޡ�
# RS232C�Хåե����ꥢ
# RS232C�ե�����
# RS�ץ���ǽ��ͭ��/̵��
# RS232C�����ǡ�������Ĺ
# UDP�����ٱ����
# �̿��ܡ��졼��
# ����饯��Ĺ
# �ѥ�ƥ��ӥå�
# ���ȥåץӥå�
%item_rssetup = (
 'rsprotocol'     => "rsprotocol",
 'rslocalport'    => "rslocalport",
 'rsremoteip1'    => "rsremoteip1",
 'rsremoteip2'    => "rsremoteip2",
 'rsremotechange' => "rsremotechange",
 'rsremoteport'   => "rsremoteport",
 'rstcpreconnect' => "rstcpreconnect",
 'rstcpclosetime' => "rstcpclosetime",
 'rsrecvtime'     => "rsrecvtime",
 'rsbufclear'     => "rsbufclear",
 'rsflow'         => "rsflow",
 'rsproconmode'   => "rsproconmode",
 'rsmaxrecvsize'  => "rsmaxrecvsize",
 'rsudpsenddelay' => "rsudpsenddelay",
 'rsspeed'        => "rsspeed",
 'rscharacterlen' => "rscharacterlen",
 'rsparitybit'    => "rsparitybit",
 'rsstopbit'      => "rsstopbit",
);

%item_def_rssetup = (
 'rsprotocol'     => "0",
 'rslocalport'    => "1111",
 'rsremoteip1'    => "0.0.0.0",
 'rsremoteip2'    => "0.0.0.0",
 'rsremotechange' => "4",
 'rsremoteport'   => "1111",
 'rstcpreconnect' => "4",
 'rstcpclosetime' => "60",
 'rsrecvtime'     => "10",
 'rsbufclear'     => "0",
 'rsflow'         => "0",
 'rsproconmode'   => "0",
 'rsmaxrecvsize'  => "1024",
 'rsudpsenddelay' => "100",
 'rsspeed'        => "19200",
 'rscharacterlen' => "8",
 'rsparitybit'    => "0",
 'rsstopbit'      => "1",

);

%error_list = (
 'rslocalport_interror' => "������ݡ����ֹ�ϡ������ǻ��ꤷ�Ƥ���������",
 'rslocalport_error'    => "������ݡ����ֹ�ϡ�1��65535�δ֤ǻ��ꤷ�Ƥ���������",
 'rsremoteip1_error'    => "�ץ饤�ޥꥻ�󥿡���IP���ɥ쥹�����꤬����������ޤ���",
 'rsremoteip2_error'    => "��������ꥻ�󥿡���IP���ɥ쥹�����꤬����������ޤ���",
 'rsremotechange_interror' => "��⡼���ڤ��ؤ�����ϡ������ǻ��ꤷ�Ƥ���������",
 'rsremotechange_error'    => "��⡼���ڤ��ؤ�����ϡ�0��10��δ֤ǻ��ꤷ�Ƥ���������",
 'rsremoteport_interror' => "��⡼�ȥݡ����ֹ�ϡ������ǻ��ꤷ�Ƥ���������",
 'rsremoteport_error'    => "��⡼�ȥݡ����ֹ�ϡ�1��65535�δ֤ǻ��ꤷ�Ƥ���������",
 'rstcpreconnect_interror' => "TCP��³��Բ���ϡ������ǻ��ꤷ�Ƥ���������",
 'rstcpreconnect_error'    => "TCP��³��Բ���ϡ�1��10�δ֤ǻ��ꤷ�Ƥ���������",
 'rstcpresend_interror'    => "TCP�ǡ���������Բ���ϡ������ǻ��ꤷ�Ƥ���������",
 'rstcpresend_error'       => "TCP�ǡ���������Բ���ϡ�1��10�δ֤ǻ��ꤷ�Ƥ���������",
 'rstcpclosetime_interror'    => "TCP���ǥ����ޡ��ϡ������ǻ��ꤷ�Ƥ���������",
 'rstcpclosetime_error'       => "TCP���ǥ����ޡ��ϡ�0�ޤ���10��9999�äδ֤ǻ��ꤷ�Ƥ���������",
 'rsrecvtime_interror'    => "RS232C���������ޡ��ϡ������ǻ��ꤷ�Ƥ���������",
 'rsrecvtime_error'       => "RS232C���������ޡ��ϡ�1��6000(x10)�ߥ��äδ֤ǻ��ꤷ�Ƥ���������",

 'rsmaxrecvsize_interror'    => "RS232C�����ǡ�������Ĺ�ϡ������ǻ��ꤷ�Ƥ���������",
 'rsmaxrecvsize_error'       => "RS232C�����ǡ�������Ĺ�ϡ�256��1460�Х��Ȥδ֤ǻ��ꤷ�Ƥ���������",
 'rsudpsenddelay_interror'    => "UDP�����ٱ���֤ϡ������ǻ��ꤷ�Ƥ���������",
 'rsudpsenddelay_error'       => "UDP�����ٱ���֤ϡ�1��6000(x10)�ߥ��äδ֤ǻ��ꤷ�Ƥ���������",
);


my $section = 'rssetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $rs_protocol_val = "";
my $rs_bufclear_val = "";
my $rs_flow_val = "";

my $rs_speed_val = "";
my $rs_characterlen_val = "";
my $rs_paritybit_val = "";
my $rs_stopbit_val = "";

&hyper::get_args($commandline);         # ���������ؿ�

if ($commandline) {
    $commandline = hyper::url_decode($commandline);
    $setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
    %items = &get_item();
    my @Keys = keys %item_rssetup;
    &hyper::cng_param(\%items, \@Keys, $commandline);

    $err_item = &chk_item(\%items);
    if ($err_item) {
        $err_item = &error_script($err_item);
    }
    else {
        &set_modify_item(%items);
    }
}
else {
    %items = &get_item();
}

my $rsproconmode_val = input_rsproconmode($items{'rsproconmode'});
$rs_protocol_val = input_rs_protocol($items{'rsprotocol'});
$rs_bufclear_val = input_rs_bufclear($items{'rsbufclear'});
$rs_flow_val = input_rs_flow($items{'rsflow'});
$rs_speed_val = input_rs_speed($items{'rsspeed'});
$rs_characterlen_val = input_rs_characterlen($items{'rscharacterlen'});
$rs_paritybit_val = input_rs_paritybit($items{'rsparitybit'});
$rs_stopbit_val = input_rs_stopbit($items{'rsstopbit'});


sub get_item {
    my %items = ();
    #g����ƤӽФ�
    %items = &hyper::get_section($section, "", \%item_rssetup, \%item_def_rssetup);
    return %items;
}

sub set_modify_item {
    my %items = @_;
    my $i;

    my @Key = keys %item_rssetup;
    my %rhash = ();
    foreach my $keyn (@Key) {
        $rhash{$item_rssetup{$keyn}} = $items{"$keyn"};
    }
    my $filename = &hyper::get_temp_file($section);
    &hyper::writefile_hush($filename, \%rhash);
    return %items;
}

sub chk_item {
    my $it = $_[0];

    # RS�ץ���ǽ��̵���ξ�硢�ʲ�������Υ����å��ϹԤ�ʤ���
    if( $items{rsproconmode} == 0 ){
        return undef;
    }
    
    # ������ݡ����ֹ�(������)
    if (&hyper::checknumstring($items{rslocalport}) == 0) {
        return "rslocalport_interror";
    }
    # ������ݡ����ֹ���ϰϡ�
    if (($items{rslocalport} < 1) || ($items{rslocalport} > 65535)) {
        return "rslocalport_error";
    }

    # �ץ饤�ޥꥻ�󥿡���IP���ɥ쥹
    if( ( $items{rsprotocol} == 1 ) || ( $items{rsprotocol} == 4 ) ){
        if (&hyper::get_ipaddress($items{rsremoteip1}) eq "") {
            return "rsremoteip1_error";
        }
    }
    else{
        if (&hyper::get_ipaddress($items{rsremoteip1}) eq "") {
            if( "$items{rsremoteip1}" eq "0.0.0.0" ){
            }
            else{
                return "rsremoteip1_error";
            }
        }
    }

    # ��������ꥻ�󥿡���IP���ɥ쥹
    if (&hyper::get_ipaddress($items{rsremoteip2}) eq "") {
        if( "$items{rsremoteip2}" eq "0.0.0.0" ){
        }
        else{
            return "rsremoteip2_error";
        }
    }

    # ��⡼���ڤ��ؤ����(������)
    if (&hyper::checknumstring($items{rsremotechange}) == 0) {
        return "rsremotechange_interror";
    }
    # ��⡼���ڤ��ؤ����(�ϰ�)
    if (($items{rsremotechange} < 0) || ($items{rsremotechange} > 10)) {
        return "rsremotechange_error";
    }

    # ��⡼�ȥݡ����ֹ�(������)
    if (&hyper::checknumstring($items{rsremoteport}) == 0) {
        return "rsremoteport_interror";
    }
    # ��⡼�ȥݡ����ֹ���ϰϡ�
    if (($items{rsremoteport} < 1) || ($items{rsremoteport} > 65535)) {
        return "rsremoteport_error";
    }
    # TCP��³��Բ��(������)
    if (&hyper::checknumstring($items{rstcpreconnect}) == 0) {
        return "rstcpreconnect_interror";
    }
    # TCP��³��Բ�����ϰϡ�
    if (($items{rstcpreconnect} < 0) || ($items{rstcpreconnect} > 10)) {
        return "rstcpreconnect_error";
    }
    # TCP���ǥ����ޡ�(������)
    if (&hyper::checknumstring($items{rstcpclosetime}) == 0) {
        return "rstcpclosetime_interror";
    }
    # TCP���ǥ����ޡ����ϰϡ�
    if ( ( $items{rstcpclosetime} != 0) && 
         ( ($items{rstcpclosetime} < 10) || ($items{rstcpclosetime} > 9999) ) ) {
        return "rstcpclosetime_error";
    }
    # RS232C���������ޡ�(������)
    if (&hyper::checknumstring($items{rsrecvtime}) == 0) {
        return "rsrecvtime_interror";
    }
    # RS232C���������ޡ����ϰϡ�
    if (($items{rsrecvtime} < 1) || ($items{rsrecvtime} > 6000)) {
        return "rsrecvtime_error";
    }

    # RS232C�����ǡ�������Ĺ(������)
    if (&hyper::checknumstring($items{rsmaxrecvsize}) == 0) {
        return "rsmaxrecvsize_interror";
    }
    # RS232C�����ǡ�������Ĺ(�ϰ�)
    if (($items{rsmaxrecvsize} < 256) || ($items{rsmaxrecvsize} > 1460)) {
        return "rsmaxrecvsize_error";
    }
    # UDP�����ٱ����(������)
    if (&hyper::checknumstring($items{rsudpsenddelay}) == 0) {
        return "rsudpsenddelay_interror";
    }
    # UDP�����ٱ����(�ϰ�)
    if (($items{rsudpsenddelay} < 1) || ($items{rsudpsenddelay} > 6000)) {
        return "rsudpsenddelay_error";
    }

    return undef;
}

sub input_rsproconmode {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"rsproconmode\">
                  <option value=\"0\" selected >̵��
                  <option value=\"1\">ͭ��
              </select> ";
    }
    else {
        $p = "<select name=\"rsproconmode\">
                  <option value=\"0\">̵��
                  <option value=\"1\" selected >ͭ��
              </select> ";
    }

    return $p;
}



sub input_rs_protocol {
    my $v = $_[0];
    my $p;

    if ("$v" eq '1') {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\" selected >TCP���饤�����
                  <option value=\"2\">TCP������
                  <option value=\"3\">UDP
                  <option value=\"4\">TCP���饤�����/������
              </select> ";
    }
    elsif ("$v" eq '2') {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\">TCP���饤�����
                  <option value=\"2\" selected >TCP������
                  <option value=\"3\">UDP
                  <option value=\"4\">TCP���饤�����/������
              </select> ";
    }
    elsif ("$v" eq '3') {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\">TCP���饤�����
                  <option value=\"2\">TCP������
                  <option value=\"3\" selected >UDP
                  <option value=\"4\">TCP���饤�����/������
              </select> ";
    }
    else {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\">TCP���饤�����
                  <option value=\"2\">TCP������
                  <option value=\"3\">UDP
                  <option value=\"4\" selected >TCP���饤�����/������
              </select> ";
    }

    return $p;
}


sub input_rs_bufclear {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"rsbufclear\">
                  <option value=\"0\" selected >̵��
                  <option value=\"1\">ͭ��
              </select> ";
    }
    else {
        $p = "<select name=\"rsbufclear\">
                  <option value=\"0\">̵��
                  <option value=\"1\" selected >ͭ��
              </select> ";
    }
    return $p;
}

sub input_rs_speed {
    my $v = $_[0];
    my $p;

    if ("$v" eq '1200') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\" selected >1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    elsif ("$v" eq '2400') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\" selected >2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    elsif ("$v" eq '4800') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\" selected >4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    elsif ("$v" eq '9600') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\" selected >9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    elsif ("$v" eq '19200') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\" selected >19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    elsif ("$v" eq '38400') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\" selected >38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    elsif ("$v" eq '57600') {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\" selected >57600bps
                  <option value=\"115200\">115200bps
              </select> ";
    }
    else {
        $p = "<select name=\"rsspeed\">
                  <option value=\"1200\">1200bps
                  <option value=\"2400\">2400bps
                  <option value=\"4800\">4800bps
                  <option value=\"9600\">9600bps
                  <option value=\"19200\">19200bps
                  <option value=\"38400\">38400bps
                  <option value=\"57600\">57600bps
                  <option value=\"115200\" selected >115200bps
              </select> ";
    }

    return $p;
}

sub input_rs_characterlen {
    my $v = $_[0];
    my $p;

    if ("$v" eq '7') {
        $p = "<select name=\"rscharacterlen\">
                  <option value=\"7\" selected >7bit
                  <option value=\"8\">8bit
              </select> ";
    }
    else {
        $p = "<select name=\"rscharacterlen\">
                  <option value=\"7\">7bit
                  <option value=\"8\" selected >8bit
              </select> ";
    }
    return $p;
}

sub input_rs_paritybit {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"rsparitybit\">
                  <option value=\"0\" selected >�ʤ�
                  <option value=\"1\">���
                  <option value=\"2\">����
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"rsparitybit\">
                  <option value=\"0\">�ʤ�
                  <option value=\"1\" selected >���
                  <option value=\"2\">����
              </select> ";
    }
    else {
        $p = "<select name=\"rsparitybit\">
                  <option value=\"0\">�ʤ�
                  <option value=\"1\">���
                  <option value=\"2\" selected >����
              </select> ";
    }
    return $p;
}

sub input_rs_stopbit {
    my $v = $_[0];
    my $p;

    if ("$v" eq '1') {
        $p = "<select name=\"rsstopbit\">
                  <option value=\"1\" selected >1bit
                  <option value=\"2\">2bit
              </select> ";
    }
    else {
        $p = "<select name=\"rsstopbit\">
                  <option value=\"1\">1bit
                  <option value=\"2\" selected >2bit
              </select> ";
    }
    return $p;
}

sub input_rs_flow {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"rsflow\">
                  <option value=\"0\" selected >̵��
                  <option value=\"1\">XON/OFF
                  <option value=\"2\">RS/CS
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"rsflow\">
                  <option value=\"0\">̵��
                  <option value=\"1\" selected >XON/OFF
                  <option value=\"2\">RS/CS
              </select> ";
    }
    else {
        $p = "<select name=\"rsflow\">
                  <option value=\"0\">̵��
                  <option value=\"1\">XON/OFF
                  <option value=\"2\" selected >RS/CS
              </select> ";
    }

    return $p;
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
$err_item
<FORM>
<H2>RS-232C�ץ�ȥ����Ѵ�����</H2>
<INPUT type="submit" name="btnSend" value="����¸"> <INPUT type="submit" name="btnRetry" value="���ľ��">
<TABLE border="1">
  <TBODY>
    <TR>
      <TH width="200">����</TH>
      <TH>������</TH>
      <TH width="200">����</TH>
    </TR>
   <TR>
      <TD width="200">RS-232C�ץ�ȥ����Ѵ���ǽ</TD>
      <TD>$rsproconmode_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">���ѥץ�ȥ���</TD>
      <TD>$rs_protocol_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">������ݡ����ֹ�</TD>
      <TD><INPUT size="8" type="text" maxlength="5" name="rslocalport" value="$items{rslocalport}"></TD>
      <TD width="200"><span style="font-size: 80%">1��65535</span></TD>
   </TR>
   <TR>
      <TD width="200">�ץ饤�ޥꥻ�󥿡�IP���ɥ쥹</TD>
      <TD><INPUT size="30" type="text" maxlength="15" name="rsremoteip1" value="$items{rsremoteip1}"></TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">��������ꥻ�󥿡�IP���ɥ쥹</TD>
      <TD><INPUT size="30" type="text" maxlength="15" name="rsremoteip2" value="$items{rsremoteip2}"></TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">��⡼���ڤ��ؤ����</TD>
      <TD><INPUT size="8" type="text" maxlength="2" name="rsremotechange" value="$items{rsremotechange}">��</TD>
      <TD width="200"><span style="font-size: 80%">0��10��</span></TD>
   </TR>
   <TR>
      <TD width="200">��⡼�ȥݡ����ֹ�</TD>
      <TD><INPUT size="8" type="text" maxlength="5" name="rsremoteport" value="$items{rsremoteport}"></TD>
      <TD width="200"><span style="font-size: 80%">1��65535</span></TD>
   </TR>
   <TR>
      <TD width="200">TCP��³��Բ��</TD>
      <TD><INPUT size="8" type="text" maxlength="2" name="rstcpreconnect" value="$items{rstcpreconnect}">��</TD>
      <TD width="200"><span style="font-size: 80%">0��10��</span></TD>
   </TR>
   <TR>
      <TD width="200">TCP̵�̿��ƻ륿���ޡ�</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rstcpclosetime" value="$items{rstcpclosetime}">��</TD>
      <TD width="200"><span style="font-size: 80%">0�ޤ���10�á�9999��</span></TD>
   </TR>
   <TR>
      <TD width="200">UDP�����ٱ����</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rsudpsenddelay" value="$items{rsudpsenddelay}"><span style="font-size: 80%">��10�ߥ���</span></TD>
      <TD width="200"><span style="font-size: 80%">1��6000 ��10�ߥ���</span></TD>
   </TR>
   <TR>
      <TD width="200">RS-232C�����ƻ륿���ޡ�</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rsrecvtime" value="$items{rsrecvtime}"><span style="font-size: 80%">��10�ߥ���</span></TD>
      <TD width="200"><span style="font-size: 80%">1��6000 ��10�ߥ���</span></TD>
   </TR>
   <TR>
      <TD width="200">RS-232C�����ǡ�������Ĺ</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rsmaxrecvsize" value="$items{rsmaxrecvsize}">�Х���</TD>
      <TD width="200"><span style="font-size: 80%">256��1460�Х���</span></TD>
   </TR>
   <TR>
      <TD width="200">RS-232C�Хåե����ꥢ</TD>
      <TD>$rs_bufclear_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232C�̿��ܡ��졼��</TD>
      <TD>$rs_speed_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232C����饯��Ĺ</TD>
      <TD>$rs_characterlen_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232C�ѥ�ƥ��ӥå�</TD>
      <TD>$rs_paritybit_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232C���ȥåץӥå�</TD>
      <TD>$rs_stopbit_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232C�ե�����</TD>
      <TD>$rs_flow_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML
