# HL100用ライブラリ
#
# 2006/2/1 新規作成
# 2006/2/20 NHK1用に変更

package hyper;

# 仕様により選択
#require "nhk.pl";
#require "nomal.pl";

%cfg_path = (#設定用パス
  "FIX"     => "../../../etc/",
  "CONFIG"  => "../../../etc/current.conf/",
  "DEFAULT" => "../../../etc/default.conf/",
  "MODIFY"  => "../../../etc/modify.conf/",
  "TEMP"    => "../../../etc/temp.conf/",
  "USB"     => "../../../var/",
  "FLAG"    => "../../../opt/flag/",
  "PASS"    => "../../../home/httpd/html/.htpasswd",
  "APPCONF" => "../../../home/httpd/app/current/",
  "APPTEMP" => "../../../home/httpd/app/temp/",
  "APPEXEC" => "../../../home/admin/app/execute/",
  "PID"     => "../../../var/run/",
);

%cfg_name = (#コンフィグファイル名
	"general"     => 'general',
	"password"    => 'password',
	"network"     => 'network',
	"wansetup"    => 'wansetup',
	"smssetup"    => 'smssetup',
	"dhcpsetup"   => 'dhcpsetup',
	"snatsetup"   => 'snatsetup',
	"filtersetup" => 'filtersetup',
	"etcsetup"    => 'etcsetup',
	"etcsetup2"   => 'etcsetup2',
	"rssetup"     => 'rssetup',
	"rsstatussetup" => 'rsstatussetup',
	"ddnssetup"   => 'ddnssetup',
	"vpn"         => 'vpn',
	"vpnsetup"    => 'vpnsetup',
	"rsapubkey"   => 'rsapubkey',
	"newkey"      => 'newkey',
	"mqttpubsetup" => 'mqttpubsetup',
	"mqttsendsetup" => 'mqttsendsetup',
	"ntpsetup"    => 'ntpsetup',
	"ca.crt"      => 'ca.crt',
	"client.crt"  => 'client.crt',
	"private.key" => 'private.key',
	"mqtt_lognum" => 'mqtt_lognum',
);

%flag_name  =( #フラグ名
	"modify"  => "conf_modify.flag",
	"default" => "conf_default.flag",
	"reboot"  => "reboot.flag",
	"update"  => "update.flag",
	"fota"    => "fota.flag",
	"change"  => "conf_change.flag",
	"setkey"  => "setkey.flag",
);


#
#	引数取得関数
#
sub get_args{ # _[0] = $command
	if ($ENV{'REQUEST_METHOD'} eq "POST"){
	# ポストの時はコンテキストの長さを取得
		read(STDIN, $_[0], $ENV{'CONTENT_LENGTH'});
	}
	else {
	#そうでないときはGETなのでクエリ取得
		$_[0] = $ENV{'QUERY_STRING'};
	}
}

sub get_args_bin{ # _[0] = $command
	if ($ENV{'REQUEST_METHOD'} eq "POST"){
	# ポストの時はコンテキストの長さを取得
		my $buf = "";
		my $read_data = "";
		my $remain = $ENV{'CONTENT_LENGTH'};
		binmode(STDIN);
		while ($remain) {
			$len = sysread(STDIN, $buf, $remain);
			if (!$len) {
				last;
			}
			$remain -= $len;
			$_[0] .= $buf;
		}
	}
	else {
	#そうでないときはGETなのでクエリ取得
		$_[0] = $ENV{'QUERY_STRING'};
	}
}


#
# adminでログインしたかチェックする
#

sub get_logincheck {
#	if ($ENV{'REMOTE_USER'} eq "admin") {
		return 1;
#	}
#	return undef;
}

#
# 引数パラメータを取得する
#
sub get_param {
	my ($prm, $cmd) = @_;
	$cmd =~ s/&sr=/#sr#/g;
	$cmd =~ s/&sig=/#sig#/g;
	$cmd =~ s/&se=/#se#/g;
	$cmd =~ s/&skn=/#skn#/g;
	foreach (split(/&/, $cmd)) {
		my ($command, $value) = split(/=/,$_,2);
		if ($command eq $prm) {
			return $value;
		}
	}
	return undef;
}

#
# 引数でパラメータを変更する
#
sub cng_param {
	my ($it, $list, $cmd) = @_;
	foreach my $keyn (@{$list}) {
		my $value = &hyper::get_param("$keyn", $cmd);
		if (defined($value)) {
			$value =~ tr/"//d; #"
			$value =~ tr/>//d; #>
			$it->{"$keyn"} = $value;
		}
	}
}

#
# URLのエンコードを行う
#
sub url_encode {
	my $enc  =$_[0];
	if ($enc) {
		$enc  =~ s/(\W)/'%' . unpack("H2", $1)/eg;
#半角スペースは + 記号へ置き換え
		$enc =~ tr/ /+/;
	}
	return $enc;
}

#
# URLデコードを行う
#
sub url_decode {
	my $dec  =$_[0];

	if ($dec) {
		$dec =~ tr/+/ /;
		$dec =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

#		$dec =~s/\r//g;
#		$dec =~s/\n//g;
	}
	return $dec;
}

sub get_imagepath {
	my $aa = $_[0];
	return $img_path{"$aa"};
}

#
# 固定設定パスを取得する
#
sub get_fix_file { #$_[0] = area
	 my $filename = $cfg_path{"FIX"}.$_[0];
	return $filename;
}

#
# 設定パスを取得する
#
sub get_config_file { #$_[0] = area
	 my $filename = $cfg_path{"CONFIG"}.$_[0];
	return $filename;
}

#
# 設定変更用パスを取得する
#
sub get_modify_file { #$_[0] = area
	 my $filename = $cfg_path{"MODIFY"}.$_[0];
	return $filename;
}
#
# 設定変更テンポラリパスを取得する
#
sub get_temp_file { #$_[0] = area
	 my $filename = $cfg_path{"TEMP"}.$_[0];
	return $filename;
}

#
# USB設定がおかれているパスを取得する
#
sub get_usb_file {# $_[0] = area
	 my $filename = $cfg_path{"USB"}.$_[0];
	return $filename;
}

#
# フラグがおかれているパスを取得する
#
sub get_flag_file {# $_[0] = area
	 my $filename = $cfg_path{"FLAG"}.$_[0];
	return $filename;
}

#
# アプリケーション設定フォルダを取得する
#
sub get_app_current {# $_[0] = area
	 my $path = $cfg_path{"APPCONF"}.$_[0];
	return $path;
}

#
# アプリケーション設定変更フォルダを取得する
#
sub get_app_temp {# $_[0] = area
	 my $path = $cfg_path{"APPTEMP"}.$_[0];
	return $path;
}

#
# PIDファイルを取得する
#
sub get_pid_file { #$_[0] = area
	 my $filename = $cfg_path{"PID"}.$_[0];
	return $filename;
}

#
#	設定ファイルをバッファに溜め込む
#
sub readfile {
	my @Buff = ();
	my $file = $_[0];
	if (-e $file) {
		open(IN, $_[0]);	# 設定ファイルオープン
		while(my $line = <IN>){	# 1ラインずつ読み込み
			$line =~ s/^[ \t\f]+//;	# 先頭の空白削除
			push(@Buff, $line);
		}
		close(IN);# 設定ファイルクローズ
		return @Buff;
	}
	return undef;
}
#
#	設定ファイルをバッファに溜め込む 2
#
sub readfile2 {
	my @Buff = ();
	my $file = $_[0];
	if (-e $file) {
		open(IN, $_[0]);	# 設定ファイルオープン
		while(my $line = <IN>){	# 1ラインずつ読み込み
#			$line =~ s/^[ \t\f]+//;	# 先頭の空白削除
			$line =~ s/^[ \f]+//;	# 先頭の空白削除
			push(@Buff, $line);
		}
		close(IN);# 設定ファイルクローズ
		return @Buff;
	}
	return undef;
}
#
#	設定ファイルをハッシュバッファに溜め込む
#
sub readfile_hash {
	my %bHash = ();
	my $file = $_[0];
	if (-e $file) {
		open(IN, $file);	# 設定ファイルオープン
		while(my $line = <IN>){	# 1ラインずつ読み込み
			$line =~s/\r//g;
			$line =~s/\n//g;

			$line =~ s/^[ \t\f]+//;	# 先頭の空白削除

			my ($command, $value) = split(/=/, $line, 2);
			if (defined($command)) {
				$bHash{$command} = $value;
			}
		}
		close(IN);# 設定ファイルクローズ
		return %bHash;
	}
	return undef;
}

#
#	セクション読み込み
#
sub get_section {
	my ($section, $number, $l, $d) = @_;

	my %items = ();
	my $i;

	# 設定呼び出し
	my $filename = &get_config_file("$section$number");
	&add_section($filename, $number,\%items, $l, $d);

	# 修正ファイルがあれば取り出す
	$filename = &get_temp_file("$section$number");
	&add_section($filename, $number,\%items, $l);

	return %items;
}

#
#	セクション読み込みと書き換え
#
sub add_section {
	#読み込みファイル名,キー番号,修正ハッシュ,変更キーハッシュリスト,デフォルト
	my ($filename, $number, $it, $li, $def) = @_;

	if (-e $filename) {
		my %hashs = &readfile_hash($filename);

		my @Key = keys %{$li};
		foreach my $keyn (@Key) {
			if (defined($hashs{$li->{$keyn}})) {
				$it->{"$keyn$number"} = $hashs{$li->{$keyn}};
			}
			else {
				if (defined($def)) {
					if (defined($def->{$keyn})) {
						$it->{"$keyn$number"} = $def->{$keyn};
					}
					else {
						$it->{"$keyn$number"} ="";
					}
				}
			}
		}
	}
	else {
		my @Key = keys %{$li};
		foreach my $keyn (@Key) {
			if (defined($def)) {
				if (defined($def->{$keyn})) {
					$it->{"$keyn$number"} = $def->{$keyn};
				}
				else {
					$it->{"$keyn$number"} ="";
				}
			}
		}
	}
}

#
# 設定ファイルを書き込む
#
sub writefile {
	my ($file, @Buff) = @_;
	if (@Buff) {
		$file = '>' . $file;
		open(OUT, $file);		# 上書きモードで最オープン
		print OUT @Buff;		# 全データ書き込み
		close(OUT);				# 終了
	}
}

#
# 設定ファイルを書き込む
#
sub writefile_hush {
	my ($file, $aa) = @_;
	my %Buf = %{$aa};
	if (%Buf) {
		my @Keys = keys %Buf;
		$file = '>' . $file;
		open(OUT, $file);		# 上書きモードで最オープン
		foreach $name (@Keys) {
			my $value  = "$name=$Buf{$name}\n";
			print OUT $value;		# 全データ書き込み
		}
		close(OUT);				# 終了
	}
}

#
#
#
sub name_check {
	my $name = $_[0];
	$name =~ s/.jpg//g;
	my $len = length $name;
	my $chknum = checknumstring($name);
	if (($len == 10) and ($chknum == 1)) {
		my $mon  = substr($name,0,2);
		my $day  = substr($name,2,2);
		my $hour = substr($name,4,2);
		my $min  = substr($name,6,2);
		my $sec  = substr($name,8,2);
		$name = "$mon/$day $hour:$min:$sec";
	}
	return $name;
}

#
# 文字数値かどうかチェックする
#
# 戻り値 1:すべて数値
#
sub checknumstring {
	if ($_[0] =~ /^[0-9]+$/) {
		if ($_[0] =~ /^0[0-9]+$/){
			return 0;
		}else{
			return 1;
		}
	}
	return 0;
}

#
# HOST名及びワークグループ名かどうかチェック
#
# 戻り値 1:半角文字英数字とアンダースコア,マイナス、スラッシュ

sub checkhoststring {

	my $name = $_[0];
	my $len = length $name;

	if (($len >31) or ($len < 1)) {
		return undef;
	}

	if ($name =~ /^[0-9a-zA-Z_\/-]+$/) {
		return 1;
	}
	return undef;
}

#
# メール送信先を取得する
#
sub get_mailto {
	my $mhandle = $_[0];
	my @mlist = ();
	if (open (MAILG, $mhandle)) {
		@mlist = <MAILG>;
		close(MAILG);
		for (my $i=0; $i < @mlist; $i++) {
			$mlist[$i] =~s/\r//g;
			$mlist[$i] =~s/\n//g;
		}
		return @mlist;
	}
	return undef;
}

#
# メール送信先を設定する
#
sub set_mailto {
	my ($mhandle, @mlist) = @_;

#	my $mhandle = $cfg_path{"MAILTO"};

	open(MAILS, "> $mhandle");		#ファイルハンドル IMGGに
	foreach my $mlist (@mlist) {
		print MAILS "$mlist\n";
	}
	close(MAILS);
}

#
# メール本文を題名を取得する
#
sub get_mailbody {
#	my $mhandle = $cfg_path{"MAILBODY"};
	my $mhandle = $_[0];
	my @mlist = ();
	my $dlist ="";
	my $subject = "Hyper Mail";

	if (open (MAILB, $mhandle)) {
		@mlist = <MAILB>;
		close(MAILB);
		for (my $i=0; $i < @mlist; $i++) {
			if ($i== 0) {
				$subject = $mlist[$i];
				$subject =~s/\r//g;
				$subject =~s/\n//g;
			}
			else {
				$dlist = $dlist.$mlist[$i];
			}
		}
#		print "ret = $subject, $dlist\n";
		return ($subject, $dlist);
	}
	return (undef, undef);
}

#
# メール本文を題名を設定する
#
sub set_mailbody {
	my ($mhandle, @mlist) = @_;
#	my @mlist = @_;
#	my $mhandle = $cfg_path{"MAILBODY"};
	my @wlist =();
	$wlist[0] = shift @mlist;
	$wlist[0] = $wlist[0]."\n";
	push @wlist, @mlist;

	open(MAILB, "> $mhandle");		#ファイルハンドル IMGGに
	print MAILB @wlist;
	close(MAILB);
}

#
# IPアドレスを取得する
#
sub get_ipaddress { #$ _[0] = 文字列address #_[1]=0をOK
	my ($adr, $zero) = @_;

	if ($adr eq ""){ # 引数が無い場合
		return;
	}
	my @my_ip = split(/\./, $adr);	#コロン区切を抜き取り配列に格納する
	if (@my_ip != 4) {
	# 個数が足りないときはエラー
		return ;
	}

	for (my $i=0 ; $i<4 ; $i++) {
		if ($my_ip[$i] !~ /^[0-9]+$/) { # 最初から最後まで0-9で書かれていない場合
			return;
		}
		if ($my_ip[$i] =~ /^0[0-9]+$/) { # 0で始まる2桁以上の数値
			return;
		}
	#}
	#for ($i=0 ; $i<4 ; $i++) {
		unless (($my_ip[$i] >= 0) && ($my_ip[$i] <= 255)) {	#ipの範囲をチェック
			return;
		}
	}
	if (($my_ip[0] == 0x00) &&
		($my_ip[1] == 0x00) &&
		($my_ip[2] == 0x00) &&
		($my_ip[3] == 0x00) ){
	#全て0が設定されている時はエラー
		return $zero;
	}
	elsif (($my_ip[0] == 0xff) &&
		   ($my_ip[1] == 0xff) &&
		   ($my_ip[2] == 0xff) &&
		   ($my_ip[3] == 0xff) ){
	#全て255が設定されている時もエラー
		return;
	}
	elsif (($my_ip[0] & 0x80) == 0x00){ # class A
		if (($my_ip[1] == 0xff) &&
			($my_ip[2] == 0xff) &&
			($my_ip[3] == 0xff) ){
			return;
		}
		elsif (($my_ip[1] == 0x00) &&
		       ($my_ip[2] == 0x00) &&
		       ($my_ip[3] == 0x00) ){
			return $zero;
		}
	}
	elsif (($my_ip[0] & 0xc0) == 0x80 ){ # class B
		if (($my_ip[2] == 0xff) &&
			($my_ip[3] == 0xff) ){
			return;
		}
		elsif (($my_ip[2] == 0x00) &&
		       ($my_ip[3] == 0x00) ){
			return $zero;
		}
	}
	elsif (($my_ip[0] & 0xe0) == 0xc0) { # class C
		if ($my_ip[3] == 0xff) {
			return;
		}
		elsif ($my_ip[3] == 0x00) {
			return $zero;
		}
	}
	else {
		return;
	}
	return 1;
}

#
# サブネットマスク設定
#
sub get_submask{ #$_[0] = サブネット

	my ($adr, $zero) = @_;

	if ($adr eq "") {
		return $zero;
	}
	@sub = split(/\./, $_[0]);

	if (@sub != 4) {
	# 個数が足りないときはエラー
		return ;
	}

	for (my $i = 0; $i < 4; $i++){
		if ($sub[$i] !~ /^[0-9]+$/) {
			return;
		}
		if ($sub[$i] =~ /^0[0-9]+$/) { # 0で始まる2桁以上の数値
			return;
		}
	#}
	#for ($i=0 ; $i<4 ; $i++) {
		unless (($sub[$i] >= 0) && ($sub[$i] <= 255)) {
			return;
		}
	}
	return 1;
}

#英数字をチェックする
sub chk_graph {
	my ($str, $max) = @_;

	if($str eq ""){
		return 1;
	}
	if($str =~ /[^\x21-\x7e]/){
		return undef;
	}
	$len = length($str);
	if($len > $max) {
		return undef;
	}
	return 1;
}

#英数字をチェックする +space
sub chk_graph2 {
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

#最初の文字をチェックする。a-z,A-Z
sub chk_initial {
	my ($str, $max) = @_;

	if($str eq ""){
		return 1;
	}
	if($str =~ /^[a-zA-Z]/){
		return 1;
	}

	return undef;
}

1;
