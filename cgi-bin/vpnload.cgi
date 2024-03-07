#!/usr/bin/perl -w
###! /usr/local/bin/perl

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/vpn.pl";

%FORM = (
 'number'      => "0",
 'btnWrite'     => "",
 'confFile'      => "",
);

%error_list = (
 '1'  => 'ファイルを指定してください。',
 '2'  => 'ファイルサイズが大き過ぎます。',
 '3'  => 'ファイルのタイプが違います。',
 '4'  => 'アップデート情報(キー)に誤りがあります。',
 '5'  => '現在のバージョンより古いバージョンを指定しました。',
 '99' => '予期せぬエラーが発生しました。',
 'nameerror'      => "接続名称(nam)は英数字16文字以内で設定してください。",
 'useerror'      => "接続有効／無効(use)は[0:無効、1:有効]で設定してください。",
 'typeerror'      => "タイプ(type)は[tunnel、transport]で設定してください。",
 'ladselerror'      => "ローカルアドレス選択(ladsel)は[0:デフォルト、1:IP指定]で設定してください。",
 'ladiperror'      => "ローカルアドレス(lad)の設定が正しくありません。（例：192.168.10.100)",
 'lsubselerror'      => "ローカルサブネットアドレス選択(lsubsel)は[0:使用しない、1:使用する]で設定してください。",
 'lsuberror'      => "ローカルサブネットアドレス(lsub)の設定が正しくありません。（例：192.168.10.100/24 または 192.168.10.100/255.255.255.0）",
 'liderror'      => "ローカルID(lid)は英数字16文字以内で設定してください。",
 'lhopselerror'      => "ローカルネクストホップ選択(lhopsel)は[0:デフォルト、1:IP指定、2:なし]で設定してください。",
 'lhoperror'      => "ローカルネクロトホップアドレス(lhop)の設定が正しくありません。（例：192.168.10.100)",
 'radselerror'      => "リモートアドレス選択(radsel)は[0:any、1:IP指定、2:ドメイン名指定]で設定してください。",
 'raderror'      => "リモートアドレス(rad)は英数字64文字以内で設定してください。",
 'rsubselerror'      => "リモートサブネットアドレス選択(rsubsel)は[0:使用しない、1:使用する]で設定してください。",
 'rsuberror'      => "リモートサブネットアドレス(rsub)の設定が正しくありません。（例：192.168.10.100/24 または 192.168.10.100/255.255.255.0）",
 'riderror'      => "リモートID(rid)は英数字16文字以内で設定してください。",
 'keyselerror'      => "認証鍵(keysek)は[secret:共有鍵方式、rsasig:公開鍵方式]で設定してください。",
 'pskerror'      => "共有鍵(psk)は英数字32文字以内で設定してください。",
 'rsaerror'      => "共有鍵(rsa)の値が不正値です。",
 'ikeselerror'      => "暗号方式フェーズ1選択(ikesel)は[0:デフォルト、1:3DES-SHA1-MODP1024、2:3DES-MD5-MODP1024、3:その他、4:不使用]で設定してください。",
 'ikeerror'      => "暗号方式フェーズ1(ike)の設定が正しくありません。",
 'espselerror'      => "暗号方式フェーズ2選択(espsel)は[0:デフォルト、1:3DES-SHA1、2:3DES-MD5、3:その他]で設定してください。",
 'esperror'      => "暗号方式フェーズ2(esp)の設定が正しくありません。",
 'pfserror'      => "PFS(pfs)は[no:チェックなし、yes:チェックあり]で設定してください。",
 'keymgerror'      => "鍵交換のマージン(keymg)は30〜3600秒の範囲で指定してください。",
 'keytmerror'      => "鍵の寿命(keytm)は0〜86400秒の範囲で指定してください。",
 'satmerror'      => "SAの寿命(satm)は0〜28800秒の範囲で指定してください。",
 'dpderror'      => "DeadPeerDetection(dpd)は[0:無効、1:有効]で設定してください。",
 'dpdacterror'      => "DPDアクション(dpdact)は[hold:維持、clear:切断、restart_by_peer:再接続]で設定してください。",
 'dpddelayerror'      => "DPD送信間隔は5〜86400秒の範囲で指定してください。",
 'dpdtmerror'      => "DPDタイムアウトは5〜86400秒の範囲で指定してください。",
 'autoerror'      => "接続方法(auto)は[start:開始、add:待機、route:イベント]で設定してください。",
 'rekeyerror'      => "リキー(rekey)は[no:なし、yes:あり]で設定してください。",
);

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

# カスタマイズパラメータ
#$upload_dir = "../../../var";  # アップロードファイルを格納するディレクトリ

# 標準入力からデータを読みだす
$buf = "";
$read_data = "";
#$commandline = "";
$number = 0;
$Writefile = "";
$ConfFile = "";

$remain = $ENV{'CONTENT_LENGTH'};
binmode(STDIN);
while ($remain) {
  $len = sysread(STDIN, $buf, $remain);
  if (!$len) {
    last;
  }
  $remain -= $len;
  $read_data .= $buf;
}


=pod
$commandline = $read_data;
if ( ! defined $commandline) {
#引数がないときは終了
	print "Location: ./general.cgi\n\n";
}

$commandline = hyper::url_decode($commandline);
$number = &hyper::get_param("number", $commandline);
$Writefile = &hyper::get_param("btnWrite", $commandline);
$ConfFile = &hyper::get_param("confFile", $commandline);
=cut
# データを解釈する
$pos1 = 0; # ヘッダ部の先頭
$pos2 = 0; # ボディ部の先頭
$pos3 = 0; # ボディ部の終端
$delimiter = "";
$max_count = 0;
$ret = "";
$tmp_file = &vpn::get_conf_file();
#ファイルを削除
 	unlink "$tmp_file";

while (1) {

	# ヘッダ処理
	$pos2 = index($read_data, "\r\n\r\n", $pos1) + 4;
	my @headers = split("\r\n", substr($read_data, $pos1, $pos2 - $pos1));
	$filename = "";
	$name = "";
	foreach (@headers) {
		if ($delimiter eq "") {
			$delimiter = $_;
		} elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"/i) {
			if ($3) {
				$filename = $3;
				if ($filename =~ /([^\\\/]+)$/) {
					$filename = $1;
				}
			}
		} elsif (/^Content-Disposition: ([^;]*); name="([^;]*)"/i) {
			$name = $2;
		}
	}

	# ボディ処理
	$pos3 = index($read_data, "\r\n$delimiter", $pos2);
	$size = $pos3 - $pos2;
	if ($filename) {
		if ($size < 2048){
		 	if (open(OUT, "> $tmp_file")) {
				binmode(OUT);
				print OUT substr($read_data, $pos2, $size);
				close(OUT);
			}
			$FORM{"confFile"} = $filename;
		}else{
			$ret = "2";
		}
	} elsif ($name) {
		$FORM{$name} = substr($read_data, $pos2, $size);
	}

	# 終了処理
	$pos1 = $pos3 + length("\r\n$delimiter");
	if (substr($read_data, $pos1, 4) eq "--\r\n") {
		# すべてのファイルの終端
		 last;
	} else {
		# 次のファイルを読み出す
		$pos1 += 2;
		if ($max_count++ > 16) { last; }
		next;
	}
}

$number = $FORM{"number"};
$Writefile = $FORM{"btnWrite"};
$ConfFile = $FORM{"confFile"};
#print "Location:./general.cgi\n\n";
#my $ret = `/opt/sbin/chk_verup`;

if ($ret eq "" && $ConfFile eq ""){
	$ret = "1";
}elsif ($ret ne "2"){
	$ret = chk_vpnfile($tmp_file);
}


sub chk_vpnfile{
	my $filename = $_[0];
	my $ret = "3";
	my %hashs = ();

	%hashs = &hyper::readfile_hash($filename);

	my @Key = &vpn::get_item_vpnsetn();
	foreach my $keyn (@Key) {
		if ( exists $hashs{"$keyn"}){
			$ret = "";
		}
	}

	if($ret eq ""){
		$ret = &chk_vpndata(\%hashs);
	}
	return $ret;
}

sub chk_radio{
	my ($v,@dt) = @_;
	my $ret = 0;

	foreach my $dt (@dt) {
		if ($v eq $dt){
			$ret = 1;
			last;
		}
	}
	return $ret;
}

sub chk_vpndata{
	my $it = $_[0];
	my $ret = 0;
	#name
	if (defined $it->{"name"}) {
		if (&hyper::chk_graph($it->{"name"}, 16) eq "" ) {
			return "nameerror";
		}
	}
	#use
	if (exists $it->{"use"}) {
		$ret = &chk_radio($it->{"use"},"0","1");
		if ($ret == 0) {
			return "useerror";
		}
	}
	#type
	if (exists $it->{"type"}) {
		$ret = &chk_radio($it->{"type"},"tunnel","transport");
		if ($ret == 0) {
			return "typeerror";
		}
	}
	#lad
	if (exists $it->{"ladsel"}) {
		$ret = &chk_radio($it->{"ladsel"},"0","1");
		if ($ret == 0) {
			return "ladselerror";
		}
	}
	if (exists $it->{"lad"}) {
		if ((length $it->{"lad"}) && (&hyper::get_ipaddress($it->{"lad"}, 1) eq "")) {
			return "ladiperror";
		}
	}
	#lsub
	if (exists $it->{"lsubsel"}) {
		$ret = &chk_radio($it->{"lsubsel"},"0","1");
		if ($ret == 0) {
			return "lsubselerror";
		}
	}
	if (exists $it->{"lsub"}) {
		if ((length $it->{"lsub"}) && (&vpn::get_subnetaddress($it->{"lsub"}, 1) eq "")) {
			return "lsuberror";
		}
	}
	#lid
	if (exists $it->{"lid"}) {
		if (&hyper::chk_graph($it->{"lid"}, 16) eq "" ) {
			return "liderror";
		}
	}
	#lhop
	if (exists $it->{"lhopsel"}) {
		$ret = &chk_radio($it->{"lhopsel"},"0","1","2");
		if ($ret == 0) {
			return "lhopselerror";
		}
	}
	if (exists $it->{"lhop"}) {
		if ((length $it->{"lhop"}) && (&hyper::get_ipaddress($it->{"lhop"}, 1) eq "")) {
			return "lhoperror";
		}
	}
	#rad
	if (exists $it->{"radsel"}) {
		$ret = &chk_radio($it->{"radsel"},"0","1","2");
		if ($ret == 0) {
			return "radselerror";
		}
	}
	if (exists $it->{"rad"}) {
		if  (&hyper::chk_graph($it->{"rad"}, 64) eq "" ) {
			return "raderror";
		}
	}
	#rsub
	if (exists $it->{"rsubsel"}) {
		$ret = &chk_radio($it->{"rsubsel"},"0","1");
		if ($ret == 0) {
			return "rsubselerror";
		}
	}
	if (exists $it->{"rsub"}) {
		if ((length $it->{"rsub"}) && (&vpn::get_subnetaddress($it->{"rsub"}, 1) eq "")) {
			return "rsuberror";
		}
	}
	#rid
	if (exists $it->{"rid"}) {
		if (&hyper::chk_graph($it->{"rid"}, 16) eq "" ) {
			return "riderror";
		}
	}
	#keysel
	if (exists $it->{"keysel"}) {
		$ret = &chk_radio($it->{"keysel"},"secret","rsasig");
		if ($ret == 0) {
			return "keyselerror";
		}
	}
	#psk
	if (exists $it->{"psk"}) {
		if (&hyper::chk_graph($it->{"psk"}, 32) eq "" ) {
			return "pskerror";
		}
	}
	#rsa
	if (exists $it->{"rsa"}) {
		if (&hyper::chk_graph($it->{"rsa"}, 600) eq "" ) {
			return "rsaerror";
		}
	}
	#ike
	if (exists $it->{"ikesel"}) {
		$ret = &chk_radio($it->{"ikesel"},"0","1","2","3","4");
		if ($ret == 0) {
			return "ikeselerror";
		}
	}
	if (exists $it->{"ike"}) {
		if ((length $it->{"ike"}) && (&hyper::chk_graph($it->{"ike"}, 32) eq "" )) {
			return "ikeerror";
		}
	}
	#esp
	if (exists $it->{"espsel"}) {
		$ret = &chk_radio($it->{"espsel"},"0","1","2","3");
		if ($ret == 0) {
			return "espselerror";
		}
	}
	if (exists $it->{"esp"}) {
		if ((length $it->{"esp"}) && (&hyper::chk_graph($it->{"esp"}, 32) eq "" )) {
			return "esperror";
		}
	}
	#pfs
	if (exists $it->{"pfs"}) {
		$ret = &chk_radio($it->{"pfs"},"no","yes");
		if ($ret == 0) {
			return "pfserror";
		}
	}
	#kyemg
	if (exists $it->{"keymg"}) {
		if (&hyper::checknumstring($it->{"keymg"}) == 0) {
			return "keymgerror";
		}
		if (($it->{"keymg"} < 30) || ($it->{"keymg"} > 3600)) {
			return "keymgerror";
		}
	}
	#kyetm
	if (exists $it->{"keytm"}) {
		if (&hyper::checknumstring($it->{"keytm"}) == 0) {
			return "keytmerror";
		}
		if (($it->{"keytm"} < 0) || ($it->{"keytm"} > 86400)) {
			return "keytmerror";
		}
	}
	#satm
	if (exists $it->{"satm"}) {
		if (&hyper::checknumstring($it->{"satm"}) == 0) {
			return "satmerror";
		}
		if (($it->{"satm"} < 0) || ($it->{"satm"} > 28800)) {
			return "satmerror";
		}
	}
	#dpd
	if (exists $it->{"dpd"}) {
		$ret = &chk_radio($it->{"dpd"},"0","1");
		if ($ret == 0) {
			return "dpderror";
		}
	}
	#dpdact
	if (exists $it->{"dpdact"}) {
		$ret = &chk_radio($it->{"dpdact"},"hold","clear","restart_by_peer");
		if ($ret == 0) {
			return "dpdacterror";
		}
	}
	#dpdtmout
	if (exists $it->{"dpdtmout"}) {
		if (&hyper::checknumstring($it->{"dpdtmout"}) == 0) {
			return "dpdtmerror";
		}
		if (($it->{"dpdtmout"} < 5) || ($it->{"dpdtmout"} > 86400)) {
			return "dpdtmerror";
		}
	}
	#dpddelay
	if (exists $it->{"dpddelay"}) {
		if (&hyper::checknumstring($it->{"dpddelay"}) == 0) {
			return "dpddelayerror";
		}
		if (($it->{"dpddelay"} < 5) || ($it->{"dpddelay"} > 86400)) {
			return "dpddelayerror";
		}
	}
	#auto
	if (exists $it->{"auto"}) {
		$ret = &chk_radio($it->{"auto"},"start","add","route");
		if ($ret == 0) {
			return "autoerror";
		}
	}
	#rekey
	if (exists $it->{"rekey"}) {
		$ret = &chk_radio($it->{"rekey"},"no","yes");
		if ($ret == 0) {
			return "rekeyerror";
		}
	}
	return undef;

}

if ($ret ne "") {

#ファイルを削除
 	unlink "$tmp_file";

print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
</HEAD>
<BODY bgcolor="#cccccc">
<H2 align="center">設定ファイルチェック</H2>
<FORM action="./vpnsetup.cgi">
<INPUT type="hidden" name="number" value="$number">
<CENTER>
<P>設定ファイルが正しくありません</P>
<P>$error_list{$ret}</P>
<P/>
<P><INPUT type="submit" name="btnReset" value="戻る"></P>
</CENTER>
</FORM>
</BODY>
</HTML>
EOFHTML

}
else {
=pod
#print "FILENAME = $filename\n";
 #if ($filename ne "") {
	$filename = "$upload_dir/$filename";
#print "FILENAME = $filename\n";
	my %hashs = ();
	%hashs = &hyper::readfile_hash($filename);
#print "hashs = $hashs{name}\n";
#print $hashs;
#	my @Key = @vpn::item_vpnsetn;
	my @Key = ();
#	&vpn::get_item_vpnsetn(\@Key);
	@Key = &vpn::get_item_vpnsetn();
	my $number = "1";
	my $pr = "number=$number";	
#	foreach my $keyn (@Key) {
	foreach my $keyn (@Key) {
		my $p = "vpn_$keyn$number=$hashs{\"$keyn\"}";
		$pr = $pr."&".$p;
    }
=cut
print "Content-Type:text/html\r\n\r\n";
print <<EOFRESTART;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<STYLE TYPE="text/css">
</STYLE>
<SCRIPT Language="JavaScript">
<!--

//　自動ジャンプ
function autoLink()
{
	location.href = "./vpnsetup.cgi?number=$number&btnWrite=1";
}
// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="autoLink();">
<H2 align="center">チャンネル更新</H2>
<FORM action="./vpnsetup.cgi">
<INPUT type="hidden" name="number" value="1">

</FORM>
</BODY>
</HTML>
EOFRESTART
}

