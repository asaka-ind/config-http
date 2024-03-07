#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

%item_passwd = (
 'USERID' => "USERID",
 'OLD_PASSWD' => "OLD_PASSWD",
 'NEW_PASSWD' => "NEW_PASSWD",
 'CHK_PASSWD' => "CHK_PASSWD",
); 

%item_passwd2 = (
 'USERID' => "USERID",
 'OLD_PASSWD' => "OLD_PASSWD",
); 

%item_def = (
 'USERID' => "admin",
 'OLD_PASSWD' => "",
 'NEW_PASSWD' => "",
 'CHK_PASSWD' => "",
); 

%error_list = (
 'useriderror'    => "�桼��ID������������ޤ���",
 'stringerror'    => "�ѥ���ɤ�4-16ʸ����Ⱦ�ѱѿ�����ǻ��ꤷ�Ƥ���������",
 'passworderror1' => "�ѥ���ɤ��㤤�ޤ���",
 'passworderror2' => "�ѥ���ɤλ���˸�꤬����ޤ���",
 'setpass'        => "OK��������¸����ѹ�����ޤ���",
);

my @salts = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

my $section = 'password';
my $commandline = "";
my %items = ();
my %usapp = ();
my $setting = "";
my $err_item ="";
my $ftp_value = "";

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Location: ./general.cgi\n\n";
}

&hyper::get_args($commandline);			# ���������ؿ�

if ($commandline) {
	$commandline = hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnSend", $commandline);
}

if ($setting ne "") {
#	%items = &parse_commandline($commandline);
	%items = &get_item();
    my @Keys = keys %item_passwd;
    &hyper::cng_param(\%items, \@Keys, $commandline);

#	%usapp = &get_pass();
	%usapp = &hyper::readfile_hash("/etc/current.conf/password");
	$err_item = chk_param(\%items, \%usapp);
	if ($err_item) {
		$err_item = error_script($err_item);
	}
	else {
		&set_modify_item(%items);

		$err_item = error_script("setpass");
	}
#	$items{USERID} = "";
#	$items{OLD_PASSWD} = "";
#	$items{NEW_PASSWD} = "";
#	$items{CHK_PASSWD} = "";
}else{
}

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
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
$err_item
<H2>�ѥ���ɹ���</H2>
<FORM action="./password.cgi" method="post">
<INPUT type="submit" name="btnSend" value="����¸" $disabled> <INPUT type="submit" name="btnRetry" value="���ľ��" $disabled>
<TABLE border="1">
  <TBODY>
    <TR>
      <TD class=normal>�桼��ID��</TD>
      <TD class=normal><INPUT size="30" type="text" maxlength="32" name="USERID" value="$items{USERID}"></TD>
    </TR>
    <TR>
      <TD class=normal>��ѥ���ɡ�</TD>
      <TD class=normal><INPUT size="30" type="password" maxlength="16" name="OLD_PASSWD" value="$items{OLD_PASSWD}"></TD>
    </TR>
    <TR>
      <TD class=normal>���ѥ���ɡ�</TD>
      <TD class=normal><INPUT size="30" type="password" maxlength="16" name="NEW_PASSWD" value="$items{NEW_PASSWD}"></TD>
    </TR>
    <TR>
      <TD class=normal>���ѥ���ɳ�ǧ��</TD>
      <TD class=normal><INPUT size="30" type="password" maxlength="16" name="CHK_PASSWD" value="$items{CHK_PASSWD}"></TD>
    </TR>
   </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML

sub error_script {
	my $error = $error_list{$_[0]};
	my $pp = "<SCRIPT LANGUAGE=\"JavaScript1.1\">\n";

	$pp = $pp."<!---\n";
	$pp = $pp."window.alert(\"$error\")\n";
	$pp = $pp."//--->\n";
	$pp = $pp."</SCRIPT>\n";
	return $pp;
}

sub get_item {
	my %items = ();
	my $i;

	#general�ƤӽФ�
	%items = &hyper::get_section($section, "", \%item_passwd, \%$item_def);
	return %items;
}

sub set_modify_item {
	my %items = @_;
	my $i;

	my @Key = keys %item_passwd2;
	my %rhash = ();
	foreach my $keyn (@Key) {
		if($keyn eq "OLD_PASSWD"){
			$rhash{$item_passwd2{$keyn}} = $items{"NEW_PASSWD"};
		}else{
			$rhash{$item_passwd2{$keyn}} = $items{"$keyn"};
		}
	}
	my $filename = &hyper::get_temp_file($section);
	&hyper::writefile_hush($filename, \%rhash);
	return %items;
}

#�ѥ�����Ѥ�ʸ���������å�����
sub chk_string {
	if($_[0] eq ""){
		return undef;
	}
	if($_[0] !~ /[[:graph:]]/){
		return undef;
	}
	$len = length($_[0]);
	if(($len > 16) || ($len < 4)) {
		return undef;
	}
	return 1;
}

#�ѥ���ɤ�����å�������������н񤭴�����
sub chk_param {
	my ($it, $up) = @_;

#	my %upass = %{$up};
#	my %items = %{$it};

	my $user ="";
	my $oldpass="";
	my $crypass="";
    my ($name, $value);

	while (($name, $value) = each(%{$up})) {
		if ($name eq "USERID") { 
			if ($it->{USERID} eq $value) {
				$user    = $value;
			}
		}
		if ($name eq "OLD_PASSWD") {
			$oldpass = $value;
		}
	}

	if ($user eq "") {
		return "useriderror";
	}

	while (($name, $value) = each(%{$it})) {
		#�ѥ���ɤ�ʸ�����������ʤ����Ͻ�λ
		#print "Name=$name,Value=$value\n";
		unless (chk_string($value)) {
			return "stringerror";
		}
	}
#	my $sss = substr($oldpass, 0,2);
#	$crypass = crypt($it->{"OLD_PASSWD"}, $sss);
	$crypass = $it->{"OLD_PASSWD"};
	if ($crypass ne $oldpass) {
	# �ѥ���ɤ����äƤʤ����ϥ��顼
		return "passworderror1";
	}

	if ($it->{NEW_PASSWD} ne $it->{CHK_PASSWD}) {
		return "passworderror2";
	}

#	my $srand = $salts[int(rand(@salts))] . $salts[int(rand(@salts))];

#	$crypass = crypt($it->{"NEW_PASSWD"}, $srand);
#	$crypass = $it->{"NEW_PASSWD"};

#	$up->{$user} = $crypass;
	return undef;
}

sub parse_commandline {
	my @pairs = split(/&/, $_[0]);
	my %items = ();

#   open(OOUT, "> c:/temp/testp.txt");
	foreach $pair (@pairs){
		my ($command, $value) = split(/=/, $pair);

#		print OOUT "$command:$value\n";

		if ($command ne "btnSend") {
			$items{$command} = $value;
		}
	}
#	close(OOUT);
	return %items;
}


sub get_pass {	#�ѥ���ɤ���Ф�

	my %hashs = ();
	if (open(IN, $hyper::cfg_path{PASS})) {
		while(my $line = <IN>){
			$line =~s/\r//g;
			$line =~s/\n//g;
			my ($keys, $value) = split(/admin:/, $line);
			$hashs{"$keys"} = $value;
		}
		close(IN);
		return %hashs;
	}
	return undef;
}

sub set_pass { # �ѥ���ɤ��ѹ�����
	my %hashs = @_;
	if (open(OUT, "> $hyper::cfg_path{PASS}")) {
		while (my ($key, $value) = each(%hashs)) {
			print OUT "$key:$value\n";
		}
		close(OUT);
	}
}

sub set_system_pass { #�����ƥ�Υѥ���ɤ��ѹ�����
	my %items = @_;

	my $command = "/opt/sbin/passwd -c $items{USERID} $items{OLD_PASSWD} $items{NEW_PASSWD} $items{CHK_PASSWD}";
	my $ret = `$command`;
	if ($ret ne "") {
		return undef;
	}
	return 1;
}
