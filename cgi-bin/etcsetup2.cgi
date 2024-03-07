#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_etcsetup2 = (
 'dnsfwd_onoff'         => "dnsfwd_onoff",
 'dscpclear_onoff'      => "dscpclear_onoff",
 'antenna'              => "antenna",
 'antenna_time'         => "antenna_time",
 'modelog'              => "modelog",
 'modelog_time'         => "modelog_time",
);

%item_def_etcsetup2 = (
 'dnsfwd_onoff'	    => "1",
 'dscpclear_onoff'      => "0",
 'antenna'              => "0",
 'antenna_time'         => "",
 'modelog'              => "0",
 'modelog_time'         => "",
);

%error_list = (
 'ddnsnameerror'     => "ダイナミックDNSドメイン名は半角英数字64文字以内で指定してください。",
 'antennatimeinterror'      => "ログ間隔は整数で指定してください。",
 'antennatimeerror'      => "ログ間隔は60〜86400秒の範囲で指定してください。",
);

my $section = 'etcsetup2';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $dnsfwd_onoff ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_etcsetup2;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
	#カレントの設定を機種別の設定に反映する。

		&set_modify_item(%items);
	}
}
else {
	%items = &get_item();
}

$dnsfwd_onoff = input_dnsfwd($items{dnsfwd_onoff});
$dscpclear_onoff = input_dscpclear($items{dscpclear_onoff});

sub chk_item {
	my %items = @_;

	if (($items{antenna_time} ne "") && (&hyper::checknumstring($items{antenna_time}) == 0)) {
		return "antennatimeinterror";
	}

	if (($items{antenna_time} ne "") && (($items{antenna_time} < 60) || ($items{antenna_time} > 86400))) {
		return "antennatimeerror";
	}

	if (($items{antenna} eq "2") && ($items{antenna_time} eq "")) {
		return "antennatimeinterror";
	}

	if (($items{modelog_time} ne "") && (&hyper::checknumstring($items{modelog_time}) == 0)) {
		return "antennatimeinterror";
	}

	if (($items{modelog_time} ne "") && (($items{modelog_time} < 60) || ($items{modelog_time} > 86400))) {
		return "antennatimeerror";
	}

	if (($items{modelog} eq "2") && ($items{modelog_time} eq "")) {
		return "antennatimeinterror";
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

sub input_dnsfwd {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"dnsfwd_onoff\" value=\"0\" checked>OFF  　　<INPUT type=\"radio\" name=\"dnsfwd_onoff\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dnsfwd_onoff\" value=\"0\" >OFF  　　<INPUT type=\"radio\" name=\"dnsfwd_onoff\" value=\"1\" checked>ON";
	}
	return $p;
}

sub input_dscpclear {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"dscpclear_onoff\" value=\"0\" checked>OFF  　　<INPUT type=\"radio\" name=\"dscpclear_onoff\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dscpclear_onoff\" value=\"0\" >OFF  　　<INPUT type=\"radio\" name=\"dscpclear_onoff\" value=\"1\" checked>ON";
	}
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
	$p = $p."　$u";

	return $p;
}


my $input_antenna = &set_radio4_pr("antenna", $items{"antenna"}, "0", "3", "1", "2", "随時", "随時(少)", "無し", "時間");
my $input_antennatime = &set_input_pr("antenna_time", $items{"antenna_time"}, "10", "5","","秒間隔");
my $input_modelog = &set_radio3_pr("modelog", $items{"modelog"}, "0", "1", "2", "随時", "無し", "時間");
my $input_modelogtime = &set_input_pr("modelog_time", $items{"modelog_time"}, "10", "5","","秒間隔");

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
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>その他設定２</H2>
<FORM name="etcsetup2" action="./etcsetup2.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="170">DNSリレー</TD>
     <TD width="170">$dnsfwd_onoff</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="170">DSCPクリア制御</TD>
     <TD width="170">$dscpclear_onoff</TD>
    </TR>
  </TBODY>
</TABLE>

<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="170">無線モードログ出力方式</TD>
     <TD width="170">$input_modelog</TD>
     <TD>$input_modelogtime</TD>
    </TR>   
  </TBODY>
</TABLE>

<BR>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="170">アンテナログ出力方式</TD>
     <TD width="270">$input_antenna</TD>
     <TD>$input_antennatime</TD>
    </TR>   
  </TBODY>
</TABLE>

</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %items = ();
	#g設定呼び出し
	%items = &hyper::get_section($section, "", \%item_etcsetup2, \%item_def_etcsetup2);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_etcsetup2;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_etcsetup2{$keyn}} = $items{"$keyn"};
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
	if($str =~ /[^\x20-\x7e]/){
		return undef;
	}
	$len = length($str);
	if($len > $max) {
		return undef;
	}
	return 1;
}

