# HL100�ѥ饤�֥��
#
# 2006/2/1 ��������
# 2006/2/20 NHK1�Ѥ��ѹ�

package hyper;

# ���ͤˤ������
#require "nhk.pl";
#require "nomal.pl";

%cfg_path = (#�����ѥѥ�
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

%cfg_name = (#����ե����ե�����̾
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

%flag_name  =( #�ե饰̾
	"modify"  => "conf_modify.flag",
	"default" => "conf_default.flag",
	"reboot"  => "reboot.flag",
	"update"  => "update.flag",
	"fota"    => "fota.flag",
	"change"  => "conf_change.flag",
	"setkey"  => "setkey.flag",
);


#
#	���������ؿ�
#
sub get_args{ # _[0] = $command
	if ($ENV{'REQUEST_METHOD'} eq "POST"){
	# �ݥ��Ȥλ��ϥ���ƥ����Ȥ�Ĺ�������
		read(STDIN, $_[0], $ENV{'CONTENT_LENGTH'});
	}
	else {
	#�����Ǥʤ��Ȥ���GET�ʤΤǥ��������
		$_[0] = $ENV{'QUERY_STRING'};
	}
}

sub get_args_bin{ # _[0] = $command
	if ($ENV{'REQUEST_METHOD'} eq "POST"){
	# �ݥ��Ȥλ��ϥ���ƥ����Ȥ�Ĺ�������
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
	#�����Ǥʤ��Ȥ���GET�ʤΤǥ��������
		$_[0] = $ENV{'QUERY_STRING'};
	}
}


#
# admin�ǥ����󤷤��������å�����
#

sub get_logincheck {
#	if ($ENV{'REMOTE_USER'} eq "admin") {
		return 1;
#	}
#	return undef;
}

#
# �����ѥ�᡼�����������
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
# �����ǥѥ�᡼�����ѹ�����
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
# URL�Υ��󥳡��ɤ�Ԥ�
#
sub url_encode {
	my $enc  =$_[0];
	if ($enc) {
		$enc  =~ s/(\W)/'%' . unpack("H2", $1)/eg;
#Ⱦ�ѥ��ڡ����� + ������֤�����
		$enc =~ tr/ /+/;
	}
	return $enc;
}

#
# URL�ǥ����ɤ�Ԥ�
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
# ��������ѥ����������
#
sub get_fix_file { #$_[0] = area
	 my $filename = $cfg_path{"FIX"}.$_[0];
	return $filename;
}

#
# ����ѥ����������
#
sub get_config_file { #$_[0] = area
	 my $filename = $cfg_path{"CONFIG"}.$_[0];
	return $filename;
}

#
# �����ѹ��ѥѥ����������
#
sub get_modify_file { #$_[0] = area
	 my $filename = $cfg_path{"MODIFY"}.$_[0];
	return $filename;
}
#
# �����ѹ��ƥ�ݥ��ѥ����������
#
sub get_temp_file { #$_[0] = area
	 my $filename = $cfg_path{"TEMP"}.$_[0];
	return $filename;
}

#
# USB���꤬������Ƥ���ѥ����������
#
sub get_usb_file {# $_[0] = area
	 my $filename = $cfg_path{"USB"}.$_[0];
	return $filename;
}

#
# �ե饰��������Ƥ���ѥ����������
#
sub get_flag_file {# $_[0] = area
	 my $filename = $cfg_path{"FLAG"}.$_[0];
	return $filename;
}

#
# ���ץꥱ�����������ե�������������
#
sub get_app_current {# $_[0] = area
	 my $path = $cfg_path{"APPCONF"}.$_[0];
	return $path;
}

#
# ���ץꥱ������������ѹ��ե�������������
#
sub get_app_temp {# $_[0] = area
	 my $path = $cfg_path{"APPTEMP"}.$_[0];
	return $path;
}

#
# PID�ե�������������
#
sub get_pid_file { #$_[0] = area
	 my $filename = $cfg_path{"PID"}.$_[0];
	return $filename;
}

#
#	����ե������Хåե���ί�����
#
sub readfile {
	my @Buff = ();
	my $file = $_[0];
	if (-e $file) {
		open(IN, $_[0]);	# ����ե����륪���ץ�
		while(my $line = <IN>){	# 1�饤�󤺤��ɤ߹���
			$line =~ s/^[ \t\f]+//;	# ��Ƭ�ζ�����
			push(@Buff, $line);
		}
		close(IN);# ����ե����륯����
		return @Buff;
	}
	return undef;
}
#
#	����ե������Хåե���ί����� 2
#
sub readfile2 {
	my @Buff = ();
	my $file = $_[0];
	if (-e $file) {
		open(IN, $_[0]);	# ����ե����륪���ץ�
		while(my $line = <IN>){	# 1�饤�󤺤��ɤ߹���
#			$line =~ s/^[ \t\f]+//;	# ��Ƭ�ζ�����
			$line =~ s/^[ \f]+//;	# ��Ƭ�ζ�����
			push(@Buff, $line);
		}
		close(IN);# ����ե����륯����
		return @Buff;
	}
	return undef;
}
#
#	����ե������ϥå���Хåե���ί�����
#
sub readfile_hash {
	my %bHash = ();
	my $file = $_[0];
	if (-e $file) {
		open(IN, $file);	# ����ե����륪���ץ�
		while(my $line = <IN>){	# 1�饤�󤺤��ɤ߹���
			$line =~s/\r//g;
			$line =~s/\n//g;

			$line =~ s/^[ \t\f]+//;	# ��Ƭ�ζ�����

			my ($command, $value) = split(/=/, $line, 2);
			if (defined($command)) {
				$bHash{$command} = $value;
			}
		}
		close(IN);# ����ե����륯����
		return %bHash;
	}
	return undef;
}

#
#	����������ɤ߹���
#
sub get_section {
	my ($section, $number, $l, $d) = @_;

	my %items = ();
	my $i;

	# ����ƤӽФ�
	my $filename = &get_config_file("$section$number");
	&add_section($filename, $number,\%items, $l, $d);

	# �����ե����뤬����м��Ф�
	$filename = &get_temp_file("$section$number");
	&add_section($filename, $number,\%items, $l);

	return %items;
}

#
#	����������ɤ߹��ߤȽ񤭴���
#
sub add_section {
	#�ɤ߹��ߥե�����̾,�����ֹ�,�����ϥå���,�ѹ������ϥå���ꥹ��,�ǥե����
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
# ����ե������񤭹���
#
sub writefile {
	my ($file, @Buff) = @_;
	if (@Buff) {
		$file = '>' . $file;
		open(OUT, $file);		# ��񤭥⡼�ɤǺǥ����ץ�
		print OUT @Buff;		# ���ǡ����񤭹���
		close(OUT);				# ��λ
	}
}

#
# ����ե������񤭹���
#
sub writefile_hush {
	my ($file, $aa) = @_;
	my %Buf = %{$aa};
	if (%Buf) {
		my @Keys = keys %Buf;
		$file = '>' . $file;
		open(OUT, $file);		# ��񤭥⡼�ɤǺǥ����ץ�
		foreach $name (@Keys) {
			my $value  = "$name=$Buf{$name}\n";
			print OUT $value;		# ���ǡ����񤭹���
		}
		close(OUT);				# ��λ
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
# ʸ�����ͤ��ɤ��������å�����
#
# ����� 1:���٤ƿ���
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
# HOST̾�ڤӥ�����롼��̾���ɤ��������å�
#
# ����� 1:Ⱦ��ʸ���ѿ����ȥ������������,�ޥ��ʥ�������å���

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
# �᡼����������������
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
# �᡼������������ꤹ��
#
sub set_mailto {
	my ($mhandle, @mlist) = @_;

#	my $mhandle = $cfg_path{"MAILTO"};

	open(MAILS, "> $mhandle");		#�ե�����ϥ�ɥ� IMGG��
	foreach my $mlist (@mlist) {
		print MAILS "$mlist\n";
	}
	close(MAILS);
}

#
# �᡼����ʸ����̾���������
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
# �᡼����ʸ����̾�����ꤹ��
#
sub set_mailbody {
	my ($mhandle, @mlist) = @_;
#	my @mlist = @_;
#	my $mhandle = $cfg_path{"MAILBODY"};
	my @wlist =();
	$wlist[0] = shift @mlist;
	$wlist[0] = $wlist[0]."\n";
	push @wlist, @mlist;

	open(MAILB, "> $mhandle");		#�ե�����ϥ�ɥ� IMGG��
	print MAILB @wlist;
	close(MAILB);
}

#
# IP���ɥ쥹���������
#
sub get_ipaddress { #$ _[0] = ʸ����address #_[1]=0��OK
	my ($adr, $zero) = @_;

	if ($adr eq ""){ # ������̵�����
		return;
	}
	my @my_ip = split(/\./, $adr);	#�������ڤ�ȴ���������˳�Ǽ����
	if (@my_ip != 4) {
	# �Ŀ���­��ʤ��Ȥ��ϥ��顼
		return ;
	}

	for (my $i=0 ; $i<4 ; $i++) {
		if ($my_ip[$i] !~ /^[0-9]+$/) { # �ǽ餫��Ǹ�ޤ�0-9�ǽ񤫤�Ƥ��ʤ����
			return;
		}
		if ($my_ip[$i] =~ /^0[0-9]+$/) { # 0�ǻϤޤ�2��ʾ�ο���
			return;
		}
	#}
	#for ($i=0 ; $i<4 ; $i++) {
		unless (($my_ip[$i] >= 0) && ($my_ip[$i] <= 255)) {	#ip���ϰϤ�����å�
			return;
		}
	}
	if (($my_ip[0] == 0x00) &&
		($my_ip[1] == 0x00) &&
		($my_ip[2] == 0x00) &&
		($my_ip[3] == 0x00) ){
	#����0�����ꤵ��Ƥ�����ϥ��顼
		return $zero;
	}
	elsif (($my_ip[0] == 0xff) &&
		   ($my_ip[1] == 0xff) &&
		   ($my_ip[2] == 0xff) &&
		   ($my_ip[3] == 0xff) ){
	#����255�����ꤵ��Ƥ�����⥨�顼
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
# ���֥ͥåȥޥ�������
#
sub get_submask{ #$_[0] = ���֥ͥå�

	my ($adr, $zero) = @_;

	if ($adr eq "") {
		return $zero;
	}
	@sub = split(/\./, $_[0]);

	if (@sub != 4) {
	# �Ŀ���­��ʤ��Ȥ��ϥ��顼
		return ;
	}

	for (my $i = 0; $i < 4; $i++){
		if ($sub[$i] !~ /^[0-9]+$/) {
			return;
		}
		if ($sub[$i] =~ /^0[0-9]+$/) { # 0�ǻϤޤ�2��ʾ�ο���
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

#�ѿ���������å�����
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

#�ѿ���������å����� +space
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

#�ǽ��ʸ��������å����롣a-z,A-Z
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
