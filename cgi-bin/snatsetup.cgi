#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

my $count = 50; #個数

my %item_list = ();
my %item_def = ();


%item_snatsetup = (
 'snatwanport' => "snatwanport",
 'snatlanip'   => "snatlanip",
 'snatlanport' => "snatlanport",
);

%item_def_snatsetup = (
 'snatwanport' => "",
 'snatlanip'   => "",
 'snatlanport' => "",
);

for (my $i = 1; $i <= $count; $i++) {
	my @Key = keys %item_snatsetup;
	foreach my $k (@Key) {
		$item_list{"$k$i"} = $item_snatsetup{"$k"}."$i";
		$item_def{"$k$i"}  = $item_def_snatsetup{"$k"};
	}
}


if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Location: ./general.cgi\n\n";
}

my $section = 'snatsetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";

&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
	%items = &get_item();
	my @Keys = keys %item_list;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		%items = sort_item(%items);
		&set_modify_item(%items);
	}
}
else {
	%items = &get_item();
}

sub sort_item {
	my %items = @_;
	my $it =();
	my $i;
	my $j = 1;
	for ($i = 1; $i <= $count; $i++) {
		my $wport = $items{"snatwanport$i"};
		my $lip   = $items{"snatlanip$i"};
		my $lport = $items{"snatlanport$i"};

		if ((length $wport) || (length $lip) || (length $lport)) {
			$it{"snatwanport$j"} = $wport;
		 	$it{"snatlanip$j"}   = $lip;
			$it{"snatlanport$j"} = $lport;
			$j++;
		}
	}
	return %it;
}

sub chk_item {
	my %items = @_;
	my $i;
	my @check = ();

	for ($i = 1; $i <=$count; $i++) {
		my $wport = $items{"snatwanport$i"};
		my $lip   = $items{"snatlanip$i"};
		my $lport = $items{"snatlanport$i"};
		if ((length $wport) || (length $lip) || (length $lport)) {
			if (&hyper::checknumstring($wport) == 0) {
				return "番号:$i WAN側ポート番号は整数で指定してください。";
			}
			if (($wport < 1) || ($wport > 65535)) {
				return "番号:$i WAN側ポート番号は1から65535の範囲で指定してください。";
			}
			if (&hyper::get_ipaddress($lip) eq "") {
				return "番号:$i LAN側IPアドレスの設定が正しくありません。";
			}
			if (&hyper::checknumstring($lport) == 0) {
				return "番号:$i LAN側ポート番号は整数で指定してください。";
			}
			if (($lport < 1) || ($lport > 65535)) {
				return "番号:$i LAN側ポート番号は1から65535の範囲で指定してください。";
			}
			for (my $j = 1; $j < $i; $j++) {
				if (($check[$j] > 0) && ($check[$j] == $wport)) {
					return "番号$jと番号$iのWAN側ポート番号が$wport番で重複しています。";
				}
			}
			$check[$i] = $wport;
		}
		else {
			$check[$i] = -1;
		}
	}
}

sub error_script {
#	my $error = $error_list{$_[0]};
	my $error = $_[0];
	my $pp = "<SCRIPT LANGUAGE=\"JavaScript1.1\">\n";

	$pp = $pp."<!---\n";
	$pp = $pp."window.alert(\"$error\")\n";
	$pp = $pp."//--->\n";
	$pp = $pp."</SCRIPT>\n";
	return $pp;
}

sub get_item {
	my %items = ();
	%items = &hyper::get_section("snatsetup", "", \%item_list, \%$item_def);
	return %items;
}

sub set_modify_item {
	my %items = @_;

	my @Key = keys %item_list;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("snatsetup");
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

sub snat_list {
	my %items = @_;
	my ($i, $p);

	$p =<<"TRHEAD";
    <TR>
      <TH width="100" align="center">番号</TH>
      <TH align="center" width="150">WAN側ポート番号</TH>
      <TH align="center" width="150">LAN側IPアドレス</TH>
      <TH align="center" width="150">LAN側ポート番号</TH>
    </TR>
TRHEAD
	for ($i=1; $i <= $count; $i++) {
	$p .=<<"TDPRINT";
    <TR>
      <TD width="100" align="center">$i</TD>
      <TD align="center" width="150"><INPUT size="20" type="text" maxlength="5" name="snatwanport$i" value=$items{"snatwanport$i"}></TD>
      <TD align="center" width="150"><INPUT size="20" type="text" maxlength="15" name="snatlanip$i"  value=$items{"snatlanip$i"}></TD>
      <TD align="center" width="150"><INPUT size="20" type="text" maxlength="5" name="snatlanport$i" value=$items{"snatlanport$i"}></TD>
    </TR>
TDPRINT
	}
	return $p;
}
$snatlist = snat_list(%items);


print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 10.0.1.0 for Windows">
<TITLE></TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>静的NAT設定</H2>
<FORM action="./snatsetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>
<TABLE border="1">
  <TBODY>
  $snatlist
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML
