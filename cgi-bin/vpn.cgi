#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/vpn.pl";

%item_list = ();
%item_def = ();

my $list_count = &vpn::get_list_count();

my $commandline = "";
my %items = ();
my $setting = "";
my $keying = "";
my $modifying = "";
my $err_item ="";
my $section = "vpnsetup";
my $number = "";
my $vpn_setkey = "";
my $setkey_tflag = &vpn::get_setkey_tflag();
my $rsapubkey_file = &vpn::get_rsapubkey_file();

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

%error_list = (
 'iferror'      => "現在のバージョンでは、VPN接続インターフェースはWANのみです。WANを設定してください。",
 'nameerror'      => "接続名称は英数字16文字以内で設定してください。",
 'name2error'      => "接続名称に同じ名前があります。",
 'name3error'      => "接続名称はアルファベット(a-zA-Z)で始まらなければいけません。",
 'natkptmerror'      => "NATキープアライブ間隔は10〜3600秒の範囲で指定してください。",
 'changekey'      => "鍵変更がチェックされています。RSA公開鍵の変更を、設定保存実行後に行います。",
);

&hyper::get_args($commandline);			# 引数取得関数
if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSet", $commandline);
	$keying = &hyper::get_param("btnKey", $commandline);

	for ($i = 1; $i <= $list_count; $i++) {
		 my $modnum = &hyper::get_param("btnModify$i" , $commandline);

		if (defined $modnum){ 
			$number = $i;
			print "Status: 302 Moved\n";
			print "Location:./vpnsetup.cgi?number=$number\n\n";
			#exit;
			last;
		 }
	}
}

&vpn::make_list(\%item_list, \%item_def);
%items = &hyper::get_section("vpnsetup", "" ,\%item_list, \%item_def);

if( -f $setkey_tflag){
	$vpn_setkey = "yes";
}

if (defined $setting) {
	my @Keys = keys %item_list;
	&hyper::cng_param(\%items, \@Keys, $commandline);
	$vpn_setkey = &hyper::get_param("vpn_setkey", $commandline);

	$err_item = &chk_item(\%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);
		if($vpn_setkey eq "yes"){
			$err_item = "changekey";
			$err_item = error_script($err_item);
			&hyper::writefile($setkey_tflag, "yes");
		}else{
			unlink($setkey_tflag);
		}
	}
}


sub chk_item {
	my $it = $_[0];
	my $i = 0;
	my $j = 0;

	if ($it->{"vpn_if"} != 1) {
		return "iferror";
	}

	if (&hyper::checknumstring($it->{"vpn_natkptm"}) == 0) {
		return "natkptmerror";
	}
	if (($it->{"vpn_natkptm"} < 10) || ($it->{"vpn_natkptm"} > 3600)) {
		return "natkptmerror";
	}

	for ($i = 1; $i <= $list_count; $i++) {
		if ($it->{"vpn_name$i"} eq "" ) {
			return "nameerror";
		}
		if (&hyper::chk_graph($it->{"vpn_name$i"}, 16) eq "" ) {
			return "nameerror";
		}
		if (&hyper::chk_initial($it->{"vpn_name$i"}, 16) eq "" ) {
			return "name3error";
		}
		for ($j = 1; $j <= $list_count; $j++) {
			if($i != $j && $it->{"vpn_name$i"}  eq $it->{"vpn_name$j"} ){
				return "name2error";
			}
		}
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

sub set_modify_item {
	my %items = @_;

	my @Key = keys %item_list;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("vpnsetup");
	&hyper::writefile_hush($filename, \%rhash);
}

my $table = &make_table(%items);

sub set_radio_pr{
	my ($name,$v,$value0,$value1,$va_pr0,$va_pr1,$en0,$en1) = @_;
	my $p = "";
	my $checked0 = "";
	my $checked1 = "";

	if("$v" eq "$value0"){
		$checked0 = "checked";
	}else{
		$checked1 = "checked";
	}
	$p = "<INPUT type=\"radio\" name=\"$name\" value=\"$value0\" $checked0 $en0>$va_pr0 ";
	$p = $p."<INPUT type=\"radio\" name=\"$name\" value=\"$value1\" $checked1 $en1>$va_pr1";
	
	return $p;
}

sub set_input_pr{
	my ($n,$v,$s,$l,$en,$u) = @_;
	my $p = "";

	$p = "<INPUT size=\"$s\" type=\"text\" maxlength=\"$l\" name=\"$n\" value=\"$v\" $en>";
	$p = $p."　$u";

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

sub setkey_pr{
	my $p;
	$p = &set_checkbox_pr("vpn_setkey", $vpn_setkey,  "yes", "鍵変更", "");	

	return $p;
}

sub getkey_pr{
	my @p;
	@p = &hyper::readfile($rsapubkey_file);	

	return $p[0];
	#return $rsapubkey_file;
}


sub make_table {
	my %items = @_;
	my $i;

	my $p =<<"THCAPTION";
    <TR>
      <TH nowrap width="50">接続</TH>
      <TH nowrap width="200">名称</TH>
      <TH nowrap width="120">VPN有効</TH>
      <TH nowrap width="80">設定変更</TH>
    </TR>
THCAPTION
	my $add = 1;
	my @color = ("bgcolor=#d0d0d0", "bgcolor=#e0e0e0");
	for ($i = 1; $i <= $list_count; $i++) {
		my $inputvpn_name = &set_input_pr("vpn_name$i", $items{"vpn_name$i"}, "31", "16", "", "");
		my $inputvpn_use = &set_radio_pr("vpn_use$i", $items{"vpn_use$i"}, "0", "1", "無効", "有効");
		$p .=<<"TDHTML";
    <TR>
      <TD align="center" valign="middle" >$i</TD>
      <TD>$inputvpn_name</TD>
     <TD>$inputvpn_use</TD>
      <TD align="center" valign="middle"><INPUT type="submit" name="btnModify$i" value="変更"></TD>
   </TR>
TDHTML
	}
	return $p;
}



my $inputvpn_use = &set_radio_pr("vpn_use", $items{"vpn_use"}, "0", "1", "無効", "有効");
my $inputvpn_if = &set_radio_pr("vpn_if", $items{"vpn_if"}, "0", "1", "LAN", "WAN", "disabled", "");
my $inputvpn_unid = &set_radio_pr("vpn_unid", $items{"vpn_unid"}, "no", "yes", "無効", "有効");
my $inputvpn_nattr = &set_radio_pr("vpn_nattr", $items{"vpn_nattr"}, "no", "yes", "無効", "有効");
my $inputvpn_natkeep = &set_radio_pr("vpn_natkeep", $items{"vpn_natkeep"}, "no", "yes", "無効", "有効");
my $inputvpn_natkptm = &set_input_pr("vpn_natkptm", $items{"vpn_natkptm"}, "10", "10","","秒");
my $inputvpn_rsa = &setkey_pr();
my $pr_vpn_rsa = &getkey_pr();

my $tb1_w1 ="width=\"180\"";
my $tb1_w2 ="width=\"200\"";

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

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
$err_item
<H2>VPN設定一覧</H2>
<FORM method="POST" action="./vpn.cgi">
<INPUT type="submit" name="btnSet" value="仮保存">　<INPUT type="submit" name="btnRetry" value="やり直し">
<TABLE border="0">
  <TBODY>
    <TR>
      <TD>
      <TABLE border="1">
        <TBODY>
          <TR>
            <TD $tb1_w1>VPN有効</TD>
            <TD $tb1_w2>$inputvpn_use</TD>
          </TR>
<!--
          <TR>
            <TD $tb1_w1>インターフェース</TD>
            <TD $tb1_w2>$inputvpn_if</TD>
          </TR>
          <TR>
            <TD $tb1_w1>ユニークID</TD>
            <TD $tb1_w2>$inputvpn_unid</TD>
          </TR>
-->
          <TR>
            <TD $tb1_w1>NATトラバーサル</TD>
            <TD $tb1_w2>$inputvpn_nattr</TD>
          </TR>
<!--
          <TR>
            <TD $tb1_w1>　NATキープアライブ</TD>
            <TD $tb1_w2>$inputvpn_natkeep</TD>
          </TR>
          <TR>
            <TD $tb1_w1>　NATキープアライブ間隔</TD>
            <TD $tb1_w2>$inputvpn_natkptm</TD>
          </TR>
-->
          <TR>
            <TD $tb1_w1>RSA公開鍵</TD>
            <TD $tb1_w2>$inputvpn_rsa</TD>
          </TR>
          <TR>
            <TD colspan="2"><textarea name="rsa" cols="55" rows="5" wrap="soft"  readonly>$pr_vpn_rsa</textarea></TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
   </TR>
　<TD></TD>
<!--
</FORM>
<FORM method="POST" action="./vpnsetup.cgi">
-->
   <TR>
      <TD>
      <TABLE  border="1" cellpadding=2>
      <TBODY>
        $table
      </TBODY>
      </TABLE>
    </TD>
   </TR>
</FORM>
  </TBODY>
</TABLE>

</BODY>
</HTML>
EOFHTML
