#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_dhcpsetup = (
 'dhcpserver'   => "dhcpserver",
 'dhcpstart'    => "dhcpstart",
 'dhcpend'      => "dhcpend",
 'dhcpsubnet'   => "dhcpsubnet",
 'dhcpgateads'  => "dhcpgateads",
 'dhcptime'     => "dhcptime",
 'dhcpdns1'     => "dhcpdns1",
 'dhcpdns2'     => "dhcpdns2",
);

%item_network = (
 'txtIPAdr1'  => "ipadr1",
 'txtSubAdr1' => "subnetadr1",
);


%item_def_dhcpsetup = (
 'dhcpserver'   => "0",
 'dhcpstart'    => "192.168.1.2",
 'dhcpend'      => "192.168.1.20",
 'dhcpsubnet'   => "255.255.255.0",
 'dhcpgateads'  => "192.168.1.1",
 'dhcptime'     => "3600",
 'dhcpdns1'     => "220.159.212.200",
 'dhcpdns2'     => "220.159.212.201",
);

%item_def_network = (
 'dhcptime'     => "168",
 'txtIPAdr1'    => "192.168.1.100",
 'txtSubAdr1'   => "255.255.255.0",
);

%item_list = (%item_dhcpsetup, %item_network);
%item_def = (%item_def_dhcpsetup, %item_def_network);

%error_list = (
 'dhcpstartadrerror'    => "配布開始IPアドレスの設定が正しくありません。",
 'dhcpendadrerror'      => "配布終了IPアドレスの設定が正しくありません。",
 'dhcpdns1adrerror'      => "配布DNSサーバ1の設定が正しくありません。",
 'dhcpdns2adrerror'      => "配布DNSサーバ2の設定が正しくありません。",
 'dhcpstartendadrerror' => "配布終了IPアドレスは配布開始アドレスより大きいアドレスを指定してください。",
 'dhcpsubmaskerror'     => "配布サブネットの設定が正しくありません。",
 'dhcpgateadserror'     => "配布デフォルトゲートウェイの設定が正しくありません。",
 'dhcptimeinterror'     => "リース時間は整数で指定してください。",
 'dhcptimeerror'        => "リース時間は1から1440分の範囲で指定してください。",
);


my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $dhcp_value = "";

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Location: ./general.cgi\n\n";
}

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();

	my @Keys  = keys %item_dhcpsetup;
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
$dhcp_value = input_dhcpserver($items{'dhcpserver'});

sub get_item {
	my %dhcp = ();
	my %nets = ();
	my %items = ();

	#DHCP設定呼び出し
	%dhcp = &hyper::get_section("dhcpsetup", "" ,\%item_dhcpsetup, \%item_def_dhcpsetup);
	#network設定呼び出し
	%nets = &hyper::get_section("network", "" ,\%item_network, \%item_def_network);

	%items = (%dhcp, %nets);
	# DHCPリース時間を分単位に変換
	my $dtime = $items{'dhcptime'} / 60;
	$items{'dhcptime'} = "$dtime";

	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_dhcpsetup;#dhcp分のみ
	my %rhash = ();
	foreach my $keyn (@Key) {
		if ($keyn eq 'dhcptime') {
		# 秒表示に変換
			$rhash{$item_dhcpsetup{$keyn}} = $items{"$keyn"} * 60;
		}
		else {
			$rhash{$item_dhcpsetup{$keyn}} = $items{"$keyn"};
		}
	}
	my $filename = &hyper::get_temp_file("dhcpsetup");
	&hyper::writefile_hush($filename, \%rhash);
}

sub chk_item {
	my $it = $_[0];
	my $use = $items{'dhcpserver'};

	if (($use eq "1") ||
		(length $items{dhcpstart}) ||
		(length $items{dhcpend})   ||
		(length $items{dhcpsubnet}) ||
		(length $items{dhcpgateads})) {
		if (&hyper::get_ipaddress($items{dhcpstart}) eq "") {
			return "dhcpstartadrerror";
		}
		if (&hyper::get_ipaddress($items{dhcpend}) eq "") {
			return "dhcpendadrerror";
		}
		if (&hyper::get_ipaddress($items{dhcpdns1}) eq "") {
			return "dhcpdns1adrerror";
		}
		if (&hyper::get_ipaddress($items{dhcpdns2}) eq "") {
			return "dhcpdns2adrerror";
		}
		my @start = split(/\./, $items{dhcpstart});
		my @end   = split(/\./, $items{dhcpend});
		my $s = ($start[0]*(2**24))+($start[1]*(2**16))+($start[2]*(2**8))+$start[3];
		my $e = ($end[0]*(2**24))+($end[1]*(2**16))+($end[2]*(2**8))+$end[3];
		if ($e < $s) {
			return "dhcpstartendadrerror";
		}
		if (&hyper::get_submask($items{dhcpsubnet}) eq "") {
			return "dhcpsubmaskerror";
		}

		if (&hyper::get_ipaddress($items{dhcpgateads}) eq "") {
			return "dhcpgateadserror";
		}
	}

	if (&hyper::checknumstring($items{dhcptime}) == 0) {
		return "dhcptimeinterror";
	}

	if (($items{dhcptime} < 1) || ($items{dhcptime} > 1440)) {
		return "dhcptimeerror";
	}
	return undef;
}

sub input_dhcpserver {
	my $v = $_[0];
	my $p;

	if ("$v" eq '0') {
		$p = "<INPUT type=\"radio\" name=\"dhcpserver\" value=\"0\" checked>OFF <INPUT type=\"radio\" name=\"dhcpserver\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"dhcpserver\" value=\"0\" >OFF <INPUT type=\"radio\" name=\"dhcpserver\" value=\"1\" checked>ON";
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
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<FORM>
<H2>DHCP設定</H2>
<INPUT type="submit" name="btnSend" value="仮保存"> <INPUT type="submit" name="btnRetry" value="やり直し">
<TABLE border="1">
  <TBODY>
   <TR>
     <TD>DHCPサーバ</TD>
     <TD>$dhcp_value</TD>
   </TR>
   <TR>
     <TD>配布開始IPアドレス</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpstart" value="$items{dhcpstart}"></TD>
   </TR>
   <TR>
     <TD>配布終了IPアドレス</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpend" value="$items{dhcpend}"></TD>
   </TR>
   <TR>
     <TD>配布サブネットマスク</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpsubnet" value="$items{dhcpsubnet}"></TD>
   </TR>
   <TR>
     <TD>配布デフォルトゲートウェイ</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpgateads" value="$items{dhcpgateads}"></TD>
   </TR>
   <TR>
     <TD>配布DNSサーバ1</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpdns1" value="$items{dhcpdns1}"></TD>
   </TR>
     <TD>配布DNSサーバ2</TD>
     <TD><INPUT size="20" type="text" maxlength="15" name="dhcpdns2" value="$items{dhcpdns2}"></TD>
   </TR>
   <TR>
     <TD>リース時間</TD>
     <TD><INPUT size="20" type="text" maxlength="4" name="dhcptime" value="$items{dhcptime}">分</TD>
   </TR>
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML
