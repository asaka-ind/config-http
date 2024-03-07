#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_general = (
 'hostname' => "hostname",
);

%item_machine = (
 'name'    => "name",
 'version' => "version",
 'kversion' => "kversion",
);

%item_serial = (
 'serial' => "serial",
 'macadr1' => "macadr1",
);

%item_list = (%item_general, %item_serial, %item_machine);


%item_def_general = (
 'hostname' => "",
);

%item_def_machine = (
 'name'    => "",
 'version' => "",
 'kversion' => "",
);

%item_def_serial = (
 'serial' => "",
 'macadr1' => "",
);

%item_def = (%item_def_general, %item_def_machine, %item_def_serial);


%error_list = (
 'hostnameerr'  => "ホスト名の設定が正しくありません。",
 'change_password'  => "ログインパスワードが初期値のままです。セキュリティ強化のために[メンテナンス] -> [パスワード変更]からパスワードを変更してください。",
);

my $commandline = "";
my %items = ();
my $setting = "";
my $settm = "";
my $err_item ="";
&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
	$settm = &hyper::get_param("btnSettm", $commandline);
	$dtime = &hyper::get_param("dtime", $commandline);
}

%items = &get_item();

if ($setting ne "") {
	my @Keys = keys %item_general;
	&hyper::cng_param(\%items, \@Keys, $commandline);

	$err_item = &chk_item(\%items);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);
	}
}

#本体時刻設定
elsif ($settm ne "") {
	if (defined($dtime)) {
		my $dcommand = "/bin/date \'$dtime\'";
		my $rev = system("$dcommand &");
		sleep(1);
		system("/sbin/hwclock -w");
	}
}
else {
	# パスワードが初期値のときにワーニングを出す
	my $file1 = "/etc/thttpd/def_httpd.conf";
	my $file2 = "/etc/thttpd/httpd.conf";
	my $user = 2;		# ファイルの2行目
	my $line1 = "";
	my $line2 = "";
	open(my $fh1, "<", $file1);
	open(my $fh2, "<", $file2);
	for(my $i=0; $i<=$user; $i++){
		$line1 = readline $fh1;
		$line2 = readline $fh2;
	}
	close($fh1);
	close($fh2);
	if($line1 eq $line2) {
		$err_item = error_script("change_password");
	}
}

my $dcommand = "date \'+%Y/%m/%d %k:%M:%S\'";
my $hltime = `$dcommand`;

my $readonly ="";
my $disabled ="";
my $kernel_ver = `cat /proc/hl320`;

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
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<META http-equiv="Content-Style-Type" content="text/css">
<SCRIPT language="JavaScript">
var chpass = false;
function time() {
var now=new Date();
year=now.getYear();
if(year<2000){year=year+1900;}
month=now.getMonth()+1;
date=now.getDate();
day=new Array("日","月","火","水","木","金","土");
day=day[now.getDay()];
hour=now.getHours();
minute=now.getMinutes();
second=now.getSeconds();
if(month<="9"){month="0"+month;};
if(date<="9"){date="0"+date;};
if(hour<="9"){hour="0"+hour;};
if(minute<="9"){minute="0"+minute;};
if(second<="9"){second="0"+second;};
document.form1.watch.value=year+"/"+month+"/"+date+" "+hour+":"+minute+":"+second;
document.form1.dtime.value=year+"."+month+"."+date+"-"+hour+":"+minute+":"+second;
setTimeout('time()',1000);
}
</SCRIPT>
<TITLE>HL Series</TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY bgcolor="#cccccc" onload="time();">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用のブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>本体設定</H2>
<FORM name="form1" method="POST" action="./general.cgi"><INPUT type="submit" name="btnSend" value="仮保存" $disabled>
<TABLE border="1" cellpadding="3">
  <TBODY>
    <TR>
      <TD width="160">本体型番</TD>
      <TD width="210">$items{'name'}</TD>
    </TR>
    <TR>
      <TD width="160">製造番号</TD>
      <TD width="210">$items{'serial'}</TD>
    </TR>
    <TR>
      <TD>バージョン</TD>
      <TD>$items{'version'} \(k$kernel_ver\)</TD>
    </TR>
    <TR>
      <TD>ホスト名</TD>
      <TD><INPUT size="31" type="text" maxlength="31" name="hostname" value="$items{hostname}" $readonly></TD>
    </TR>
<!--
    <TR>
      <TD>本体時刻</TD>
      <TD>$hltime</TD>
    </TR> 
   <TR>
      <TD>現在時刻(PCの時計)</TD>
      <TD><INPUT name="watch" size="31" readonly>
          <INPUT type="submit" name="btnSettm" value="時刻設定" $disabled>
          <INPUT type="hidden" name="dtime" value="">
      </TD>
    </TR>
-->
  </TBODY>
</TABLE>
<p/>

</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %items = ();
	my $i;

	#general設定呼び出し
	my $filename = &hyper::get_config_file("general");
	&hyper::add_section($filename,"" ,\%items, \%item_list, \%item_def);

	my $hs= `hostname`;
	$hs =~s/\r//g;
	$hs =~s/\n//g;
	$items{hostname} = $hs;

	# 修正ファイルがあれば取り出す
	$filename = &hyper::get_temp_file("general");
	&hyper::add_section($filename, "", \%items, \%item_list);

	#.serialファイルを取得
	$filename = &hyper::get_fix_file(".serial");
	&hyper::add_section($filename, "", \%items, \%item_serial);

	#.machineファイルを取得
	$filename = &hyper::get_fix_file(".machine");
	&hyper::add_section($filename, "", \%items, \%item_machine);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_general;#general分のみ
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_list{$keyn}} = $items{"$keyn"};
	}
	my $filename = &hyper::get_temp_file("general");
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

sub chk_item {
	my $it = $_[0];

#	$it->{hostname} = uc $it->{hostname};
	my $d =&hyper::checkhoststring($it->{hostname});
	if ($d eq "") {
		return "hostnameerr";
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

