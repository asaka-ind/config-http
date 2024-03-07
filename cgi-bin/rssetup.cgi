#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

# 使用プロトコル
# ローカルポート番号
# プライマリセンターのIPアドレス
# セカンダリセンターのIPアドレス
# リモート切り替え回数
# リモートポート番号
# TCP接続試行回数
# TCP切断タイマー
# RS232C受信タイマー
# RS232Cバッファクリア
# RS232Cフロー制御
# RSプロコン機能の有効/無効
# RS232C受信データ最大長
# UDP送信遅延時間
# 通信ボーレート
# キャラクタ長
# パリティビット
# ストップビット
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
 'rslocalport_interror' => "ローカルポート番号は、整数で指定してください。",
 'rslocalport_error'    => "ローカルポート番号は、1〜65535の間で指定してください。",
 'rsremoteip1_error'    => "プライマリセンターのIPアドレスの設定が正しくありません。",
 'rsremoteip2_error'    => "セカンダリセンターのIPアドレスの設定が正しくありません。",
 'rsremotechange_interror' => "リモート切り替え回数は、整数で指定してください。",
 'rsremotechange_error'    => "リモート切り替え回数は、0〜10回の間で指定してください。",
 'rsremoteport_interror' => "リモートポート番号は、整数で指定してください。",
 'rsremoteport_error'    => "リモートポート番号は、1〜65535の間で指定してください。",
 'rstcpreconnect_interror' => "TCP接続試行回数は、整数で指定してください。",
 'rstcpreconnect_error'    => "TCP接続試行回数は、1〜10の間で指定してください。",
 'rstcpresend_interror'    => "TCPデータ再送試行回数は、整数で指定してください。",
 'rstcpresend_error'       => "TCPデータ再送試行回数は、1〜10の間で指定してください。",
 'rstcpclosetime_interror'    => "TCP切断タイマーは、整数で指定してください。",
 'rstcpclosetime_error'       => "TCP切断タイマーは、0または10〜9999秒の間で指定してください。",
 'rsrecvtime_interror'    => "RS232C受信タイマーは、整数で指定してください。",
 'rsrecvtime_error'       => "RS232C受信タイマーは、1〜6000(x10)ミリ秒の間で指定してください。",

 'rsmaxrecvsize_interror'    => "RS232C受信データ最大長は、整数で指定してください。",
 'rsmaxrecvsize_error'       => "RS232C受信データ最大長は、256〜1460バイトの間で指定してください。",
 'rsudpsenddelay_interror'    => "UDP送信遅延時間は、整数で指定してください。",
 'rsudpsenddelay_error'       => "UDP送信遅延時間は、1〜6000(x10)ミリ秒の間で指定してください。",
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

&hyper::get_args($commandline);         # 引数取得関数

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
    #g設定呼び出し
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

    # RSプロコン機能が無効の場合、以下の設定のチェックは行わない。
    if( $items{rsproconmode} == 0 ){
        return undef;
    }
    
    # ローカルポート番号(整数型)
    if (&hyper::checknumstring($items{rslocalport}) == 0) {
        return "rslocalport_interror";
    }
    # ローカルポート番号（範囲）
    if (($items{rslocalport} < 1) || ($items{rslocalport} > 65535)) {
        return "rslocalport_error";
    }

    # プライマリセンターのIPアドレス
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

    # セカンダリセンターのIPアドレス
    if (&hyper::get_ipaddress($items{rsremoteip2}) eq "") {
        if( "$items{rsremoteip2}" eq "0.0.0.0" ){
        }
        else{
            return "rsremoteip2_error";
        }
    }

    # リモート切り替え回数(整数型)
    if (&hyper::checknumstring($items{rsremotechange}) == 0) {
        return "rsremotechange_interror";
    }
    # リモート切り替え回数(範囲)
    if (($items{rsremotechange} < 0) || ($items{rsremotechange} > 10)) {
        return "rsremotechange_error";
    }

    # リモートポート番号(整数型)
    if (&hyper::checknumstring($items{rsremoteport}) == 0) {
        return "rsremoteport_interror";
    }
    # リモートポート番号（範囲）
    if (($items{rsremoteport} < 1) || ($items{rsremoteport} > 65535)) {
        return "rsremoteport_error";
    }
    # TCP接続試行回数(整数型)
    if (&hyper::checknumstring($items{rstcpreconnect}) == 0) {
        return "rstcpreconnect_interror";
    }
    # TCP接続試行回数（範囲）
    if (($items{rstcpreconnect} < 0) || ($items{rstcpreconnect} > 10)) {
        return "rstcpreconnect_error";
    }
    # TCP切断タイマー(整数型)
    if (&hyper::checknumstring($items{rstcpclosetime}) == 0) {
        return "rstcpclosetime_interror";
    }
    # TCP切断タイマー（範囲）
    if ( ( $items{rstcpclosetime} != 0) && 
         ( ($items{rstcpclosetime} < 10) || ($items{rstcpclosetime} > 9999) ) ) {
        return "rstcpclosetime_error";
    }
    # RS232C受信タイマー(整数型)
    if (&hyper::checknumstring($items{rsrecvtime}) == 0) {
        return "rsrecvtime_interror";
    }
    # RS232C受信タイマー（範囲）
    if (($items{rsrecvtime} < 1) || ($items{rsrecvtime} > 6000)) {
        return "rsrecvtime_error";
    }

    # RS232C受信データ最大長(整数型)
    if (&hyper::checknumstring($items{rsmaxrecvsize}) == 0) {
        return "rsmaxrecvsize_interror";
    }
    # RS232C受信データ最大長(範囲)
    if (($items{rsmaxrecvsize} < 256) || ($items{rsmaxrecvsize} > 1460)) {
        return "rsmaxrecvsize_error";
    }
    # UDP送信遅延時間(整数型)
    if (&hyper::checknumstring($items{rsudpsenddelay}) == 0) {
        return "rsudpsenddelay_interror";
    }
    # UDP送信遅延時間(範囲)
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
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else {
        $p = "<select name=\"rsproconmode\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }

    return $p;
}



sub input_rs_protocol {
    my $v = $_[0];
    my $p;

    if ("$v" eq '1') {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\" selected >TCPクライアント
                  <option value=\"2\">TCPサーバ
                  <option value=\"3\">UDP
                  <option value=\"4\">TCPクライアント/サーバ
              </select> ";
    }
    elsif ("$v" eq '2') {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\">TCPクライアント
                  <option value=\"2\" selected >TCPサーバ
                  <option value=\"3\">UDP
                  <option value=\"4\">TCPクライアント/サーバ
              </select> ";
    }
    elsif ("$v" eq '3') {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\">TCPクライアント
                  <option value=\"2\">TCPサーバ
                  <option value=\"3\" selected >UDP
                  <option value=\"4\">TCPクライアント/サーバ
              </select> ";
    }
    else {
        $p = "<select name=\"rsprotocol\">
                  <option value=\"1\">TCPクライアント
                  <option value=\"2\">TCPサーバ
                  <option value=\"3\">UDP
                  <option value=\"4\" selected >TCPクライアント/サーバ
              </select> ";
    }

    return $p;
}


sub input_rs_bufclear {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"rsbufclear\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else {
        $p = "<select name=\"rsbufclear\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
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
                  <option value=\"0\" selected >なし
                  <option value=\"1\">奇数
                  <option value=\"2\">偶数
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"rsparitybit\">
                  <option value=\"0\">なし
                  <option value=\"1\" selected >奇数
                  <option value=\"2\">偶数
              </select> ";
    }
    else {
        $p = "<select name=\"rsparitybit\">
                  <option value=\"0\">なし
                  <option value=\"1\">奇数
                  <option value=\"2\" selected >偶数
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
                  <option value=\"0\" selected >無効
                  <option value=\"1\">XON/OFF
                  <option value=\"2\">RS/CS
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"rsflow\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >XON/OFF
                  <option value=\"2\">RS/CS
              </select> ";
    }
    else {
        $p = "<select name=\"rsflow\">
                  <option value=\"0\">無効
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
<H2>RS-232Cプロトコル変換設定</H2>
<INPUT type="submit" name="btnSend" value="仮保存"> <INPUT type="submit" name="btnRetry" value="やり直し">
<TABLE border="1">
  <TBODY>
    <TR>
      <TH width="200">項目</TH>
      <TH>設定値</TH>
      <TH width="200">備考</TH>
    </TR>
   <TR>
      <TD width="200">RS-232Cプロトコル変換機能</TD>
      <TD>$rsproconmode_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">使用プロトコル</TD>
      <TD>$rs_protocol_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">ローカルポート番号</TD>
      <TD><INPUT size="8" type="text" maxlength="5" name="rslocalport" value="$items{rslocalport}"></TD>
      <TD width="200"><span style="font-size: 80%">1〜65535</span></TD>
   </TR>
   <TR>
      <TD width="200">プライマリセンターIPアドレス</TD>
      <TD><INPUT size="30" type="text" maxlength="15" name="rsremoteip1" value="$items{rsremoteip1}"></TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">セカンダリセンターIPアドレス</TD>
      <TD><INPUT size="30" type="text" maxlength="15" name="rsremoteip2" value="$items{rsremoteip2}"></TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">リモート切り替え回数</TD>
      <TD><INPUT size="8" type="text" maxlength="2" name="rsremotechange" value="$items{rsremotechange}">回</TD>
      <TD width="200"><span style="font-size: 80%">0〜10回</span></TD>
   </TR>
   <TR>
      <TD width="200">リモートポート番号</TD>
      <TD><INPUT size="8" type="text" maxlength="5" name="rsremoteport" value="$items{rsremoteport}"></TD>
      <TD width="200"><span style="font-size: 80%">1〜65535</span></TD>
   </TR>
   <TR>
      <TD width="200">TCP接続試行回数</TD>
      <TD><INPUT size="8" type="text" maxlength="2" name="rstcpreconnect" value="$items{rstcpreconnect}">回</TD>
      <TD width="200"><span style="font-size: 80%">0〜10回</span></TD>
   </TR>
   <TR>
      <TD width="200">TCP無通信監視タイマー</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rstcpclosetime" value="$items{rstcpclosetime}">秒</TD>
      <TD width="200"><span style="font-size: 80%">0または10秒〜9999秒</span></TD>
   </TR>
   <TR>
      <TD width="200">UDP送信遅延時間</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rsudpsenddelay" value="$items{rsudpsenddelay}"><span style="font-size: 80%">×10ミリ秒</span></TD>
      <TD width="200"><span style="font-size: 80%">1〜6000 ×10ミリ秒</span></TD>
   </TR>
   <TR>
      <TD width="200">RS-232C受信監視タイマー</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rsrecvtime" value="$items{rsrecvtime}"><span style="font-size: 80%">×10ミリ秒</span></TD>
      <TD width="200"><span style="font-size: 80%">1〜6000 ×10ミリ秒</span></TD>
   </TR>
   <TR>
      <TD width="200">RS-232C受信データ最大長</TD>
      <TD><INPUT size="8" type="text" maxlength="4" name="rsmaxrecvsize" value="$items{rsmaxrecvsize}">バイト</TD>
      <TD width="200"><span style="font-size: 80%">256〜1460バイト</span></TD>
   </TR>
   <TR>
      <TD width="200">RS-232Cバッファクリア</TD>
      <TD>$rs_bufclear_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232C通信ボーレート</TD>
      <TD>$rs_speed_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232Cキャラクタ長</TD>
      <TD>$rs_characterlen_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232Cパリティビット</TD>
      <TD>$rs_paritybit_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232Cストップビット</TD>
      <TD>$rs_stopbit_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
   <TR>
      <TD width="200">RS-232Cフロー制御</TD>
      <TD>$rs_flow_val</TD>
      <TD width="200">&nbsp; </TD>
   </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML
