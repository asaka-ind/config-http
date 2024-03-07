#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

# Command & Message

%item_rsstatussetup = (
 'close_cmd_ena'       => "close_cmd_ena",
 'close_cmd'           => "close_cmd",
 'start_msg_ena'       => "start_msg_ena",
 'start_msg'           => "start_msg",
 'comm_msg_ena'        => "comm_msg_ena",
 'comm_msg'            => "comm_msg",
 'close_msg_ena'       => "close_msg_ena",

 'close_msg'           => "close_msg",
 'atiniterror_msg_ena' => "atiniterror_msg_ena",
 'atiniterror_msg'     => "atiniterror_msg",
 'atout_msg_ena'       => "atout_msg_ena",
 'atout_msg'           => "atout_msg",
 'atdelay_msg_ena'     => "atdelay_msg_ena",
 'atdelay_msg'         => "atdelay_msg",
 'dialerror_msg_ena'   => "dialerror_msg_ena",
 'dialerror_msg'       => "dialerror_msg",
 'ppperror_msg_ena'    => "ppperror_msg_ena",
 'ppperror_msg'        => "ppperror_msg",
 'er_signal'           => "er_signal",
 'dr_signal'           => "dr_signal",
 'cd_signal'           => "cd_signal",
 'cs_signal'           => "cs_signal",
 'ci_signal'           => "ci_signal",


);

%item_def_rsstatussetup = (
 'close_cmd_ena'       => "0",
 'close_cmd'           => "C03",
 'start_msg_ena'       => "0",
 'start_msg'           => "*R01*",
 'comm_msg_ena'        => "0",
 'comm_msg'            => "*R02*",
 'close_msg_ena'       => "0",

 'close_msg'           => "*R04*",
 'atiniterror_msg_ena' => "0",
 'atiniterror_msg'     => "*E01*",
 'atout_msg_ena'       => "0",
 'atout_msg'           => "*E02*",
 'atdelay_msg_ena'     => "0",
 'atdelay_msg'         => "*E03*",
 'dialerror_msg_ena'   => "0",
 'dialerror_msg'       => "*E04*",
 'ppperror_msg_ena'    => "0",
 'ppperror_msg'        => "*E05*",
 'er_signal'           => "0",
 'dr_signal'           => "2",
 'cd_signal'           => "2",
 'cs_signal'           => "0",
 'ci_signal'           => "1",

);

%error_list = (
 'close_cmd_error'   => "接続先APNは半角英数字5文字以内で指定してください。",
 'start_msg_error'     => "本装置起動完了メッセージは半角英数字20文字以内で指定してください。",
 'comm_msg_error'     => "接続完了メッセージは半角英数字20文字以内で指定してください。",
 'close_msg_error'     => "回線切断メッセージは半角英数字20文字以内で指定してください。",
 'dialerror_msg_error'     => "回線接続エラーメッセージは半角英数字20文字以内で指定してください。",
);

my $section = 'rsstatussetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";

&hyper::get_args($commandline);         # 引数取得関数

if ($commandline) {
    $commandline = hyper::url_decode($commandline);
    $setting = hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
    %items = &get_item();
    my @Keys = keys %item_rsstatussetup;
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

sub chk_item {
    my %items = @_;

    if (&chk_graph($items{close_cmd}, 5) eq "" ) {
        return "close_cmd_error";
    }
    if (&chk_graph($items{start_msg}, 20) eq "" ) {
        return "start_msg_error";
    }
    if (&chk_graph($items{comm_msg}, 20) eq "" ) {
        return "comm_msg_error";
    }
    if (&chk_graph($items{close_msg}, 20) eq "" ) {
        return "close_msg_error";
    }
    if (&chk_graph($items{dialerror_msg}, 20) eq "" ) {
        return "dialerror_msg_error";
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

my $readonly ="";
my $disabled ="";
if (!&hyper::get_logincheck()) {
    $disabled = "disabled";
    $readonly = "readonly";
}


# 回線切断コマンドの有効/無効
my $close_cmd_val = input_close_cmd_value($items{'close_cmd_ena'});
sub input_close_cmd_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"close_cmd_ena\">
                  <option value=\"0\" selected > 無効
                  <option value=\"1\"> 有効
              </select> ";
    }
    else{
        $p = "<select name=\"close_cmd_ena\">
                  <option value=\"0\"> 無効
                  <option value=\"1\" selected > 有効
              </select> ";
    }
    return $p;
}

# 本装置起動完了メッセージの有効/無効
my $start_msg_val = input_start_msg_value($items{'start_msg_ena'});
sub input_start_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"start_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"start_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}

# 接続完了メッセージの有効/無効
my $comm_msg_val = input_comm_msg_value($items{'comm_msg_ena'});
sub input_comm_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"comm_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"comm_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}


# 回線切断メッセージの有効/無効
my $close_msg_val = input_close_msg_value($items{'close_msg_ena'});
sub input_close_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"close_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"close_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}

# ATコマンド初期化不良メッセージの有効/無効
my $atiniterror_msg_val = input_atiniterror_msg_value($items{'atiniterror_msg_ena'});
sub input_atiniterror_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"atiniterror_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"atiniterror_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}

# パケット圏外メッセージの有効/無効
my $atout_msg_val = input_atout_msg_value($items{'atout_msg_ena'});
sub input_atout_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"atout_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"atout_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}

# 再発信規制メッセージの有効/無効
my $atdelay_msg_val = input_atdelay_msg_value($items{'atdelay_msg_ena'});
sub input_atdelay_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"atdelay_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"atdelay_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}

# 回線接続エラーの有効/無効
my $dialerror_msg_val = input_dialerror_msg_value($items{'dialerror_msg_ena'});
sub input_dialerror_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"dialerror_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"dialerror_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}

# PPP認証エラーの有効/無効
my $ppperror_msg_val = input_ppperror_msg_value($items{'ppperror_msg_ena'});
sub input_ppperror_msg_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"ppperror_msg_ena\">
                  <option value=\"0\" selected >無効
                  <option value=\"1\">有効
              </select> ";
    }
    else{
        $p = "<select name=\"ppperror_msg_ena\">
                  <option value=\"0\">無効
                  <option value=\"1\" selected >有効
              </select> ";
    }
    return $p;
}


# ER信号制御
my $er_signal_val = input_er_signal_value($items{'er_signal'});
sub input_er_signal_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"er_signal\">
                  <option value=\"0\" selected >無視する
                  <option value=\"1\">ON->OFFでTCP切断
              </select> ";
    }
    else{
        $p = "<select name=\"er_signal\">
                  <option value=\"0\">無視する
                  <option value=\"1\" selected >ON->OFFでTCP切断
              </select> ";
    }
    return $p;
}

# DR信号制御
my $dr_signal_val = input_dr_signal_value($items{'dr_signal'});
sub input_dr_signal_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"dr_signal\">
                  <option value=\"0\" selected >常にON
                  <option value=\"1\">常にOFF
                  <option value=\"2\">TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
                  <option value=\"3\">データ受信可能中ON
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"dr_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\" selected >常にOFF
                  <option value=\"2\">TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
                  <option value=\"3\">データ受信可能中ON
              </select> ";
    }
    elsif ("$v" eq '2') {
        $p = "<select name=\"dr_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\">常にOFF
                  <option value=\"2\" selected >TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
                  <option value=\"3\">データ受信可能中ON
              </select> ";
    }
    else{
        $p = "<select name=\"dr_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\">常にOFF
                  <option value=\"2\">TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
                  <option value=\"3\" selected >データ受信可能中ON
              </select> ";
    }

    return $p;
}

# CD信号制御
my $cd_signal_val = input_cd_signal_value($items{'cd_signal'});
sub input_cd_signal_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"cd_signal\">
                  <option value=\"0\" selected >常にON
                  <option value=\"1\">常にOFF
                  <option value=\"2\">TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"cd_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\" selected >常にOFF
                  <option value=\"2\">TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
              </select> ";
    }
    else{
        $p = "<select name=\"cd_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\">常にOFF
                  <option value=\"2\" selected >TCP設定時はTCP接続中ON、UDP設定時はPPP接続中ON
              </select> ";
    }

    return $p;
}

# CS信号制御
my $cs_signal_val = input_cs_signal_value($items{'cs_signal'});
sub input_cs_signal_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"cs_signal\">
                  <option value=\"0\" selected >常にON
                  <option value=\"1\">常にOFF
              </select> ";
    }
    else{
        $p = "<select name=\"cs_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\" selected >常にOFF
              </select> ";
    }

    return $p;
}


# CI信号制御
my $ci_signal_val = input_ci_signal_value($items{'ci_signal'});
sub input_ci_signal_value {
    my $v = $_[0];
    my $p;

    if ("$v" eq '0') {
        $p = "<select name=\"ci_signal\">
                  <option value=\"0\" selected >常にON
                  <option value=\"1\">常にOFF
              </select> ";
    }
    elsif ("$v" eq '1') {
        $p = "<select name=\"ci_signal\">
                  <option value=\"0\">常にON
                  <option value=\"1\" selected >常にOFF
              </select> ";
    }

    return $p;
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
<H2>メッセージ&信号線</H2>
<FORM name="rsstatussetup" action="./rsstatussetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
      <TH width="200">項目</TH>
      <TH>設定値</TH>
      <TH width="200">備考</TH>
    </TR>
    <TR>
      <TD colspan="3">動作メッセージ</TD>
    </TR>
    <TR>
      <TD width="200">本装置起動完了</TD>
      <TD> $start_msg_val <INPUT type="text" size="31" maxlength="20" name="start_msg" value="$items{start_msg}" $readonly></TD>
      <TD width="200"><span style="font-size: 80%">最大20文字</span></TD>
    </TR>
    <TR>
      <TD width="200">接続完了</TD>
      <TD> $comm_msg_val <INPUT type="text" size="31" maxlength="20" name="comm_msg" value="$items{comm_msg}" $readonly></TD>
      <TD width="200"><span style="font-size: 80%">最大20文字</span></TD>
    </TR>
    <TR>
      <TD width="200">回線切断</TD>
      <TD> $close_msg_val <INPUT type="text" size="31" maxlength="20" name="close_msg" value="$items{close_msg}" $readonly></TD>
      <TD width="200"><span style="font-size: 80%">最大20文字</span></TD>
    </TR>
    <TR>
      <TD width="200">回線接続エラー</TD>
      <TD> $dialerror_msg_val <INPUT type="text" size="31" maxlength="20" name="dialerror_msg" value="$items{dialerror_msg}" $readonly></TD>
      <TD width="200"><span style="font-size: 80%">最大20文字</span></TD>
    </TR>
    <TR>
      <TD colspan="3">RS-232C信号線制御</TD>
    </TR>
    <TR>
      <TD width="200">ER信号</TD>
      <TD>$er_signal_val</TD>
      <TD width="200">&nbsp;</TD>
    </TR>
    <TR>
      <TD width="200">DR信号</TD>
      <TD>$dr_signal_val</TD>
      <TD width="200">&nbsp;</TD>
    </TR>
    <TR>
      <TD width="200">CD信号</TD>
      <TD>$cd_signal_val</TD>
      <TD width="200">&nbsp;</TD>
    </TR>
    <TR>
      <TD width="200">CS信号</TD>
      <TD>$cs_signal_val</TD>
      <TD width="200">&nbsp;</TD>
    </TR>
    <TR>
      <TD width="200">CI信号</TD>
      <TD>$ci_signal_val</TD>
      <TD width="200">&nbsp;</TD>
    </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
    my %items = ();
    # 設定呼び出し
    %items = &hyper::get_section($section, "", \%item_rsstatussetup, \%item_def_rsstatussetup);
    return %items;
}

sub set_modify_item {
    my %items = @_;
    my $i;

    my @Key = keys %item_rsstatussetup;
    my %rhash = ();
    foreach my $keyn (@Key) {
        $rhash{$item_rsstatussetup{$keyn}} = $items{"$keyn"};
    }
    my $filename = &hyper::get_temp_file($section);
    &hyper::writefile_hush($filename, \%rhash);
    return %items;
}

#英数字をチェックする
sub chk_graph {
    my ($str, $max) = @_;

    if($str eq ""){
        return 1;
    }
    if($str !~ /[[:graph:]]/){
        return undef;
    }
    $len = length($str);
    if($len > $max) {
        return undef;
    }
    return 1;
}


