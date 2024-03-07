#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/filter.pl";

%item_list = ();
%item_def = ();

my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $number = 0;
my $mode = "";
my $type = "";
my $section = "filtersetup";

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

&filter::make_list(\%item_list, \%item_def);

%error_list = (
 'waniperror'      => "WAN側IPアドレスの設定が正しくありません。",
 'wansubneterror'  => "WAN側サブネットマスクの設定が正しくありません。",
 'wanportinterror' => "WAN側ポート番号は整数で指定してください。",
 'wanporterror'    => "WAN側ポート番号は1から65535の範囲で指定してください。",
 'wanportszerror'  => "WAN側ポート番号の範囲の設定が正しくありません。",
 'laniperror'      => "LAN側IPアドレスの設定が正しくありません。",
 'lansubneterror'  => "LAN側サブネットマスクの設定が正しくありません。",
 'lanportinterror' => "LAN側ポート番号は整数で指定してください。",
 'lanporterror'    => "LAN側ポート番号は指定しないか、1から65535の範囲で指定してください。",
 'lanportszerror'  => "LAN側ポート番号の範囲の設定が正しくありません。",
 'configerror'    => "IPアドレスかポート番号を指定してください。",
);
&hyper::get_args($commandline);			# 引数取得関数
#$commandline="btnModify1=1&type=view";

if ($commandline eq "") {
#引数がないときは終了
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

$commandline = hyper::url_decode($commandline);
$type = &hyper::get_param("type", $commandline);

if ($type eq "set") {
#filtersetup.cgiより
	$number = &hyper::get_param("number", $commandline);

	my $m = &hyper::get_param("btnSet", $commandline);
	if ($m) {
		$mode = "set";
	}
	$m = &hyper::get_param("btnDelete", $commandline);
	if ($m) {
		$mode = "delete";
	}
}
elsif ($type eq "view") {
#filterview.cgiより
	my $m;
	for ($i=1; $i <= $filter::list_count; $i++) {
		$m = &hyper::get_param("btnModify$i", $commandline);
		if ($m) {
			$mode = "modify";
			$number = $i;
			last;
		}
		$m = &hyper::get_param("btnDelete$i", $commandline);
		if ($m) {
			$mode = "delete";
			$number = $i;
			last;
		}

		$m = &hyper::get_param("btnUp$i", $commandline);
		if ($m) {
			$mode = "up";
			$number = $i;
			last;
		}
	}
}

if (!$number || ($mode eq "")) {
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

%items = &hyper::get_section("filtersetup", "" ,\%item_list, \%item_def);

if ($mode eq "up") {
#アイテムを上に移動
	if ($number > 1) {
		my $mv = $number-1;
		my %it = (
		 'filtuse'     => $items{"filtuse$number"},
		 'filtset'     => $items{"filtset$number"},
		 'filtsel'     => $items{"filtsel$number"},
		 'filtproto'   => $items{"filtproto$number"},
		 'filtwanip'   => $items{"filtwanip$number"},
		 'filtwanmask' => $items{"filtwanmask$number"},
		 'filtwanport' => $items{"filtwanport$number"},
		 'filtlanip'   => $items{"filtlanip$number"},
		 'filtlanmask' => $items{"filtlanmask$number"},
		 'filtlanport' => $items{"filtlanport$number"},
		);
		$items{"filtuse$number"}     = $items{"filtuse$mv"};
		$items{"filtset$number"}     = $items{"filtset$mv"};
		$items{"filtsel$number"}     = $items{"filtsel$mv"};
		$items{"filtproto$number"}   = $items{"filtproto$mv"};
		$items{"filtwanip$number"}   = $items{"filtwanip$mv"};
		$items{"filtwanmask$number"} = $items{"filtwanmask$mv"};
		$items{"filtwanport$number"} = $items{"filtwanport$mv"};
		$items{"filtlanip$number"}   = $items{"filtlanip$mv"};
		$items{"filtlanmask$number"} = $items{"filtlanmask$mv"};
		$items{"filtlanport$number"} = $items{"filtlanport$mv"};

		$items{"filtuse$mv"}     = $it{"filtuse"};
		$items{"filtset$mv"}     = $it{"filtset"};
		$items{"filtsel$mv"}     = $it{"filtsel"};
		$items{"filtproto$mv"}   = $it{"filtproto"};
		$items{"filtwanip$mv"}   = $it{"filtwanip"};
		$items{"filtwanmask$mv"} = $it{"filtwanmask"};
		$items{"filtwanport$mv"} = $it{"filtwanport"};
		$items{"filtlanip$mv"}   = $it{"filtlanip"};
		$items{"filtlanmask$mv"} = $it{"filtlanmask"};
		$items{"filtlanport$mv"} = $it{"filtlanport"};
	}
	&set_modify_item(%items);
	print "Status: 302 Moved\n";
	print "Location: ./filterview.cgi\n\n";
	#exit;
}
elsif ($mode eq "delete") {
#アイテムを削除
	if ($number > 0) {
		my ($i,$j);
		for ($i=$number; $i <= $filter::list_count; $i++) {
			$j = $i+1;
			if ($i == $filter::list_count) {
				$items{"filtuse$i"}     = "";
				$items{"filtset$i"}     = "";
				$items{"filtsel$i"}     = "";
				$items{"filtproto$i"}   = "";
				$items{"filtwanip$i"}   = "";
				$items{"filtwanmask$i"} = "";
				$items{"filtwanport$i"} = "";
				$items{"filtlanip$i"}   = "";
				$items{"filtlanmask$i"} = "";
				$items{"filtlanport$i"} = "";
			}
			else {
				$items{"filtuse$i"}     = $items{"filtuse$j"};
				$items{"filtset$i"}     = $items{"filtset$j"};
				$items{"filtsel$i"}     = $items{"filtsel$j"};
				$items{"filtproto$i"}   = $items{"filtproto$j"};
				$items{"filtwanip$i"}   = $items{"filtwanip$j"};
				$items{"filtwanmask$i"} = $items{"filtwanmask$j"};
				$items{"filtwanport$i"} = $items{"filtwanport$j"};
				$items{"filtlanip$i"}   = $items{"filtlanip$j"};
				$items{"filtlanmask$i"} = $items{"filtlanmask$j"};
				$items{"filtlanport$i"} = $items{"filtlanport$j"};
			}
		}
	}
	&set_modify_item(%items);
	print "Status: 302 Moved\n";
	print "Location: ./filterview.cgi\n\n";
	#exit;
}
elsif ($mode eq "set") {
	my @Keys = keys %item_list;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(\%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);
		print "Status: 302 Moved\n";
		print "Location: ./filterview.cgi\n\n";
		#exit;
	}
}
elsif ($mode eq "modify") {
;
}
else {
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

sub set_modify_item {
	my %items = @_;

	my @Key = keys %item_list;#
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("filtersetup");
	&hyper::writefile_hush($filename, \%rhash);
}

sub chk_item {
	my $it = $_[0];
	my $port;
	my $portold;
	my @portit;
	my $portnum;

	if ((length $it->{"filtwanip$number"}) && (&hyper::get_ipaddress($it->{"filtwanip$number"}, 1) eq "")) {
		return "waniperror";
	}

	if ((length $it->{"filtwanmask$number"}) && (&hyper::get_submask($it->{"filtwanmask$number"}) eq "")) {
		return "wansubneterror";
	}

	if (length $it->{"filtwanport$number"}) {
		@portit = split( /:/,$it->{"filtwanport$number"});
		$portnum = @portit;
		if($portnum > 2){
			return "wanportinterror";
		}

		$portold = 0;
		foreach $port(@portit){
			if (&hyper::checknumstring($port) == 0) {
				return "wanportinterror";
			}

			if (($port < 1) || ($port > 65535)) {
				return "wanporterror";
			}
			if ($port <= $portold) {
 				return "wanportszerror";
			}
			$portold = $port;
		}
	}
	if ((length $it->{"filtlanip$number"}) && (&hyper::get_ipaddress($it->{"filtlanip$number"}, 1) eq "")) {
		return "laniperror";
	}
	if ((length $it->{"filtlanmask$number"}) && (&hyper::get_submask($it->{"filtlanmask$number"}) eq "")) {
		return "lansubneterror";
	}
	if (length $it->{"filtlanport$number"}) {
		@portit = split( /:/,$it->{"filtlanport$number"});
		$portnum = @portit;
		if($portnum > 2){
			return "lanportinterror";
		}

		$portold = 0;
		foreach $port(@portit){
			if (&hyper::checknumstring($port) == 0) {
				return "lanportinterror";
			}
			if (($port < 1) || ($port > 65535)) {
				return "lanporterror";
			}
			if ($port <= $portold) {
 				return "lanportszerror";
			}
			$portold = $port;
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

sub input_filtuse {
	my $v = $_[0];
	my $p;

	if (("$v" eq '0') || (length $v == 0)) {
		$p = "<INPUT type=\"radio\" name=\"filtuse$number\" value=\"0\" checked>無効　<INPUT type=\"radio\" name=\"filtuse$number\" value=\"1\">有効　";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"filtuse$number\" value=\"0\" >無効 <INPUT type=\"radio\" name=\"filtuse$number\" value=\"1\" checked>有効　";
	}
	return $p;
}

sub opt_filtsel {
	my $value = $_[0];
	my $p = "<SELECT name=\"filtsel$number\">";
	for (my $i=0; $i < @filter::opt_filtsel; $i++) {
		if ($i eq $value) {
			$p = $p."<OPTION value=\"$i\" selected>$filter::opt_filtsel[$i]</OPTION>\n";
		}
		else {
			$p = $p."<OPTION value=\"$i\">$filter::opt_filtsel[$i]</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_filtproto {
	my $value = $_[0];

	my $p = "<SELECT name=\"filtproto$number\">";
	for (my $i=0; $i < @filter::opt_filtproto; $i++) {
		if ($i eq $value) {
			$p = $p."<OPTION value=\"$i\" selected>$filter::opt_filtproto[$i]</OPTION>\n";
		}
		else {
			$p = $p."<OPTION value=\"$i\">$filter::opt_filtproto[$i]</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_filtset {
	my $value = $_[0];

	my $p = "<SELECT name=\"filtset$number\">";
	for (my $i=0; $i < @filter::opt_filtset; $i++) {
		if ($i eq $value) {
			$p = $p."<OPTION value=\"$i\" selected>$filter::opt_filtset[$i]</OPTION>\n";
		}
		else {
			$p = $p."<OPTION value=\"$i\">$filter::opt_filtset[$i]</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

my $inputfiltuse = &input_filtuse($items{"filtuse$number"});
my $optfiltsel   = &opt_filtsel($items{"filtsel$number"});
my $optfiltproto = &opt_filtproto($items{"filtproto$number"});
my $optfiltset   = &opt_filtset($items{"filtset$number"});

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
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>フィルタ設定</H2>
<FORM method="POST" action="./filtersetup.cgi">
<INPUT type="hidden" name="mode" value="1">
<INPUT type="submit" name="btnSet" value="仮保存">　<INPUT type="submit" name="btnDelete" value="削除">
<INPUT type="hidden" name="type" value="set">
<INPUT type="hidden" name="number" value="$number">
<TABLE border="0">
  <TBODY>
    <TR>
      <TD>
      <TABLE border="1">
        <TBODY>
          <TR>
            <TD width="150" colspan="2">フィルタ設定</TD>
          </TR>
          <TR>
            <TD width="150">フィルタ動作：</TD>
            <TD width="150">$inputfiltuse</TD>
          </TR>
          <TR>
            <TD width="150">パケットの向き：</TD>
            <TD width="150">$optfiltsel</TD>
          </TR>
          <TR>
            <TD width="150">プロトコル：</TD>
            <TD width="150">$optfiltproto</TD>
          </TR>
          <TR>
            <TD width="150">通信：</TD>
            <TD width="150">$optfiltset</TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD></TD>
   </TR>
   <TR><TD><TABLE border="1">
        <TBODY>
          <TR>
            <TD width="150" colspan="2">WAN側設定</TD>
          </TR>
          <TR>
            <TD width="150">IPアドレス：</TD>
            <TD width="150"><INPUT size="20" type="text" maxlength="15" name="filtwanip$number" value=$items{"filtwanip$number"}></TD>
          </TR>
          <TR>
            <TD width="150">サブネットマスク：</TD>
            <TD width="150"><INPUT size="20" type="text" maxlength="15" name="filtwanmask$number" value=$items{"filtwanmask$number"}></TD>
          </TR>
          <TR>
            <TD width="150">ポート番号：</TD>
            <TD width="150"><INPUT size="20" type="text" maxlength="11" name="filtwanport$number" value=$items{"filtwanport$number"}></TD>
          </TR>
        </TBODY>
      </TABLE>
     </TD>
     <TD><TABLE border="1">
        <TBODY>
          <TR>
            <TD width="150" colspan="2">LAN側設定</TD>
          </TR>
          <TR>
            <TD width="150">IPアドレス：</TD>
            <TD width="150"><INPUT size="20" type="text" maxlength="15" name="filtlanip$number" value=$items{"filtlanip$number"}></TD>
          </TR>
          <TR>
            <TD width="150">サブネットマスク：</TD>
            <TD width="150"><INPUT size="20" type="text" maxlength="15" name="filtlanmask$number" value=$items{"filtlanmask$number"}></TD>
          </TR>
          <TR>
            <TD width="150">ポート番号：</TD>
            <TD width="150"><INPUT size="20" type="text" maxlength="11" name="filtlanport$number" value=$items{"filtlanport$number"}></TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD></TR></TBODY></TABLE>
</BODY>
</HTML>
EOFHTML
