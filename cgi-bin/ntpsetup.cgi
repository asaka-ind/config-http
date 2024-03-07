#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_ntpsetup = (
 'ntpserver'	    => "ntpserver",
 'ntp_onoff'	    => "ntp_onoff",
 'reboot1_onoff'    => "reboot1_onoff",
 'reboot2_onoff'    => "reboot2_onoff",
 'month1'	    => "month1",
 'day1'		    => "day1",
 'hour1'	    => "hour1",
 'minute1'	    => "minute1",
 'week1'	    => "week1",
 'month2'	    => "month2",
 'day2'		    => "day2",
 'hour2'	    => "hour2",
 'minute2'	    => "minute2",
 'week2'	    => "week2",
);

%item_def_ntpsetup = (
 'ntpserver'	    => "ntp3.jst.mfeed.ad.jp",
 'ntp_onoff'	    => "1",
 'reboot1_onoff'    => "0",
 'reboot2_onoff'    => "0",
 'month1'	    => "*",
 'day1'		    => "*",
 'hour1'	    => "*",
 'minute1'	    => "59",
 'week1'	    => "*",
 'month2'	    => "*",
 'day2'		    => "*",
 'hour2'	    => "*",
 'minute2'	    => "59",
 'week2'	    => "*",
);

%error_list = (
 'ntpservererror'     => "NTPサーバ名は半角英数字64文字以内で指定してください。",
 'cronerror'     => "定時リブート機能を使うには、NTPクライアントを有効にしてください。",
);

my $section = 'ntpsetup';
my $commandline = "";
my %items = ();
my $setting = "";
my $settm = "";
my $err_item ="";
my $ntp_onoff ="";


&hyper::get_args($commandline);			# 引数取得関数

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
	$settm = &hyper::get_param("btnSettm", $commandline);
	$dtime = &hyper::get_param("dtime", $commandline);
}

%items = &get_item();

if ($setting ne "") {
	my @Keys = keys %item_ntpsetup;
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

#本体時刻設定
elsif ($settm ne "") {
	if (defined($dtime)) {
		my $dcommand = "/bin/date \'$dtime\'";
		my $rev = system("$dcommand &");
		sleep(1);
		system("/sbin/hwclock -w");
	}
}

my $dcommand = "date \'+%Y/%m/%d %k:%M:%S\'";
my $hltime = `$dcommand`;


$ntp_onoff = input_ntp($items{ntp_onoff});
$reboot1_onoff = input_reboot1($items{reboot1_onoff});
$reboot2_onoff = input_reboot2($items{reboot2_onoff});

sub chk_item {
	my %items = @_;

	if (&chk_graph($items{ntpserver}, 64) eq "" ) {
		return "ntpservererror";
	}

#	if (($items{ntp_onoff} eq "0") and ($items{reboot1_onoff} eq "1")) {
#		return "cronerror";
#	}

#	if (($items{ntp_onoff} eq "0") and ($items{reboot2_onoff} eq "1")) {
#		return "cronerror";
#	}

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

sub input_ntp {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"ntp_onoff\" value=\"0\" checked>OFF  　　<INPUT type=\"radio\" name=\"ntp_onoff\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"ntp_onoff\" value=\"0\" >OFF  　　<INPUT type=\"radio\" name=\"ntp_onoff\" value=\"1\" checked>ON";
	}
	return $p;
}

sub input_reboot1 {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"reboot1_onoff\" value=\"0\" checked>OFF  　　<INPUT type=\"radio\" name=\"reboot1_onoff\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"reboot1_onoff\" value=\"0\" >OFF  　　<INPUT type=\"radio\" name=\"reboot1_onoff\" value=\"1\" checked>ON";
	}
	return $p;
}

sub input_reboot2 {
	my $v = $_[0];
	my $p;

	if ("$v" eq "0") {
		$p = "<INPUT type=\"radio\" name=\"reboot2_onoff\" value=\"0\" checked>OFF  　　<INPUT type=\"radio\" name=\"reboot2_onoff\" value=\"1\">ON";
	}
	else {
		$p = "<INPUT type=\"radio\" name=\"reboot2_onoff\" value=\"0\" >OFF  　　<INPUT type=\"radio\" name=\"reboot2_onoff\" value=\"1\" checked>ON";
	}
	return $p;
}

my $readonly ="";
my $disabled ="";
if (!&hyper::get_logincheck()) {
	$disabled = "disabled";
	$readonly = "readonly";
}


my $optmonth1sel = &opt_monthsel($items{"month1"},1);
my $optmonth2sel = &opt_monthsel($items{"month2"},2);
my $optday1sel = &opt_daysel($items{"day1"},1);
my $optday2sel = &opt_daysel($items{"day2"},2);
my $opthour1sel = &opt_hoursel($items{"hour1"},1);
my $opthour2sel = &opt_hoursel($items{"hour2"},2);
my $optminute1sel = &opt_minutesel($items{"minute1"},1);
my $optminute2sel = &opt_minutesel($items{"minute2"},2);
my $optweek1sel = &opt_weeksel($items{"week1"},1);
my $optweek2sel = &opt_weeksel($items{"week2"},2);

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
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
document.ntpsetup.watch.value=year+"/"+month+"/"+date+" "+hour+":"+minute+":"+second;
document.ntpsetup.dtime.value=year+"."+month+"."+date+"-"+hour+":"+minute+":"+second;
setTimeout('time()',1000);
}
</SCRIPT>
<TITLE></TITLE>
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY bgcolor="#cccccc" onload="time();">
<noscript><p><font color="red">このページはJavaScriptを使用しています。 ご利用の
ブラウザはJavaScriptが無効になっているか、JavaScriptに対応していません。JavaScriptを有効にするか、JavaScriptが使用可能なブラウザでアクセスして下さい。</font></p></noscript>
$err_item
<H2>NTP設定</H2>
<FORM name="ntpsetup" action="./ntpsetup.cgi" method="post">
<INPUT type="submit" name="btnSend" value="仮保存" $disabled> <INPUT type="submit" name="btnRetry" value="やり直し" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="170">NTPクライアント</TD>
     <TD width="170">$ntp_onoff</TD>
    </TR>

    <TR>
      <TD>NTPサーバ名</TD>
      <TD><INPUT type="text" name="ntpserver" size="31" maxlength="64" value="$items{ntpserver}" $readonly></TD>
    </TR>

    <TR>
      <TD>本体時刻</TD>
      <TD>$hltime</TD>
    </TR> 
<!--
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

<BR>
定時リブート機能
<TABLE border="1">
  <TBODY>
    <TR>
     <TD width="150">定時リブート１</TD>
     <TD width="370">$reboot1_onoff</TD>
    </TR>
    <TR>
     <TD width="150">.  時刻設定</TD>
     <TD width="370">$optminute1sel分　$opthour1sel時　$optday1sel日　$optmonth1sel月　$optweek1sel曜日</TD>
    </TR>
    <TR>
     <TD width="150">定時リブート２</TD>
     <TD width="370">$reboot2_onoff</TD>
    </TR>
    <TR>
     <TD width="150">.  時刻設定</TD>
     <TD width="400">$optminute2sel分　$opthour2sel時　$optday2sel日　$optmonth2sel月　$optweek2sel曜日</TD>
    </TR>
    <TR>
  </TBODY>
</TABLE>

</FORM>
</BODY>
</HTML>
EOFHTML


sub get_item {
	my %items = ();
	#g設定呼び出し
	%items = &hyper::get_section($section, "", \%item_ntpsetup, \%item_def_ntpsetup);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_ntpsetup;
	my %rhash = ();
	foreach my $keyn (@Key) {
		$rhash{$item_ntpsetup{$keyn}} = $items{"$keyn"};
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

sub opt_monthsel {
	my $value = $_[0];
	my $v2 = $_[1];
	my @num   = ("*","1","2","3","4","5","6","7","8","9","10","11","12");
	my @type   = ("*","1","2","3","4","5","6","7","8","9","10","11","12");
	my $i;
	my $t;
	my $p = "<SELECT name=\"month$v2\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=month$v2 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=month$v2 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_daysel {
	my $value = $_[0];
	my $v2 = $_[1];
	my @num   = ("*","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31");
	my @type   = ("*","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31");
	my $i;
	my $t;
	my $p = "<SELECT name=\"day$v2\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=day$v2 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=day$v2 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_weeksel {
	my $value = $_[0];
	my $v2 = $_[1];
	my @num   = ("*","1","2","3","4","5","6","7");
	my @type   = ("*","月","火","水","木","金","土","日");
	my $i;
	my $t;
	my $p = "<SELECT name=\"week$v2\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=week$v2 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=week$v2 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_minutesel {
	my $value = $_[0];
	my $v2 = $_[1];
	my @num   = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59");
	my @type   = ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59");
	my $i;
	my $t;
	my $p = "<SELECT name=\"minute$v2\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=minute$v2 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=minute$v2 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

sub opt_hoursel {
	my $value = $_[0];
	my $v2 = $_[1];
	my @num   = ("*","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23");
	my @type   = ("*","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23");
	my $i;
	my $t;
	my $p = "<SELECT name=\"hour$v2\">";
	foreach my $i (@num) {
		$t = shift @type;
		if ($i eq $value) {
			$p = $p."<OPTION name=hour$v2 value=\"$i\" selected>$t</OPTION>\n";
		}
		else {
			$p = $p."<OPTION name=hour$v2 value=\"$i\">$t</OPTION>\n";
		}
	}
	$p = $p."</SELECT>\n";
	return $p;
}

