#!/usr/bin/perl -w
###! /usr/local/bin/perl

require "hyper.pl";

%FORM = (
 'number'      => "0",
 'btnWrite'     => "",
 'confFile'      => "",
);

%error_list = (
 '1'  => 'ファイルを指定してください。',
 '2'  => 'ファイルサイズが大き過ぎます。',
 '3'  => 'ファイルのタイプが違います。(private.key)',
 '4'  => 'アップデート情報(キー)に誤りがあります。',
 '5'  => '現在のバージョンより古いバージョンを指定しました。',
 '99' => '予期せぬエラーが発生しました。',
);

if (!&hyper::get_logincheck()) {
# adminでないならTOPに戻す
	print "Location: ./general.cgi\n\n";
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
$tmp_file = "/tmp/private.key.tmp";
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
		if ($filename ne "private.key") {
			$ret = "3";
		}	
		if ($size < 100000){
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
}elsif ($ret ne "2" && $ret ne "3"){
	$ret = "";
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
<H2 align="center">ファイルチェック</H2>
<FORM action="./privatefile.cgi">
<INPUT type="hidden" name="number" value="$number">
<CENTER>
<P>ファイルが正しくありません</P>
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
	location.href = "./privatefile.cgi?&btnWrite=1";
}
// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="autoLink();">
<H2 align="center">チャンネル更新</H2>
<FORM action="./privatefile.cgi">
<INPUT type="hidden" name="number" value="1">

</FORM>
</BODY>
</HTML>
EOFRESTART
}

