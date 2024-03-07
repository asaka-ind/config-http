package vpn;

require "/home/httpd/cgi-bin/hyper.pl";

$list_count = 5;

$conf_file = "../../../tmp/vpn_conf.tmp";
$setkey_tflag = "../../../tmp/setkey.flag";
$rsapubkey_file = "../../../etc/current.conf/rsapubkey";

%item_vpn = (
 'vpn_use'      => "vpn_use",
 'vpn_if'          => "vpn_if",
 'vpn_unid'     => "vpn_unid",
 'vpn_nattr'    => "vpn_nattr",
 'vpn_natkeep'    => "vpn_natkeep",
 'vpn_natkptm'    => "vpn_natkptm",
);

%item_def_vpn = (
 'vpn_use'     => "no",
 'vpn_if'         => "1",
 'vpn_unid'    => "yes",
 'vpn_nattr'   => "no",
 'vpn_natkeep'    => "yes",
 'vpn_natkptm'    => "30",
);

%item_vpnset = (
 'vpn_name'	=> "vpn_name",
 'vpn_use'	=> "vpn_use",
 'vpn_mode'	=> "vpn_mode",
 'vpn_type'	=> "vpn_type",
 'vpn_ladsel'	=> "vpn_ladsel",
 'vpn_lad'	=> "vpn_lad",
 'vpn_lsubsel'	=> "vpn_lsubsel",
 'vpn_lsub'	=> "vpn_lsub",
 'vpn_lid'	=> "vpn_lid",
 'vpn_lhopsel'	=> "vpn_lhopsel",
 'vpn_lhop'	=> "vpn_lhop",
 'vpn_radsel'	=> "vpn_radsel",
 'vpn_rad'	=> "vpn_rad",
 'vpn_rsubsel'	=> "vpn_rsubsel",
 'vpn_rsub'	=> "vpn_rsub",
 'vpn_rid'	=> "vpn_rid",
 'vpn_keysel'	=> "vpn_keysel",
 'vpn_psk'	=> "vpn_psk",
 'vpn_rsa'	=> "vpn_rsa",
 'vpn_ikesel'	=> "vpn_ikesel",
 'vpn_ike'	=> "vpn_ike",
 'vpn_espsel'	=> "vpn_espsel",
 'vpn_esp'	=> "vpn_esp",
 'vpn_pfs'	=> "vpn_pfs",
 'vpn_keymg'	=> "vpn_keymg",
 'vpn_satm'	=> "vpn_satm",
 'vpn_keytm'	=> "vpn_keytm",
 'vpn_dpd'	=> "vpn_dpd",
 'vpn_dpddelay'	=> "vpn_dpddelay",
 'vpn_dpdtmout'	=> "vpn_dpdtmout",
 'vpn_dpdact'	=> "vpn_dpdact",
 'vpn_auto'	=> "vpn_auto",
 'vpn_rekey'	=> "vpn_rekey",
);

%item_def_vpnset = (
 'vpn_name'	=> "",
 'vpn_use'	=> "tunnel",
 'vpn_mode'	=> "main",
 'vpn_type'	=> "0",
 'vpn_ladsel'	=> "0",
 'vpn_lad'	=> "",
 'vpn_lsubsel'	=> "0",
 'vpn_lsub'	=> "",
 'vpn_lid'	=> "",
'vpn_lhopsel'	=> "0",
 'vpn_lhop'	=> "",
 'vpn_radsel'	=> "0",
 'vpn_rad'	=> "",
 'vpn_rsubsel'	=> "0",
 'vpn_rsub'	=> "",
 'vpn_rid'	=> "",
 'vpn_keysel'	=> "secret",
 'vpn_psk'	=> "",
 'vpn_rsa'	=> "",
 'vpn_ikesel'	=> "0",
 'vpn_ike'	=> "",
 'vpn_espsel'	=> "0",
 'vpn_esp'	=> "",
 'vpn_pfs'	=> "no",
 'vpn_keymg'	=> "540",
 'vpn_satm'	=> "3600",
 'vpn_keytm'	=> "7200",
 'vpn_dpd'	=> "0",
 'vpn_dpddelay'	=> "30",
 'vpn_dpdtmout'	=> "120",
 'vpn_dpdact'	=> "restart",
 'vpn_auto'	=> "start",
 'vpn_rekey'	=> "yes",
);

@item_vpnsetn = (
 'name',
 'use',
 'mode',
 'type',
 'ladsel',
 'lad',
 'lsubsel',
 'lsub',
 'lid',
 'lhopsel',
 'lhop',
 'radsel',
 'rad',
 'rsubsel',
 'rsub',
 'rid',
 'keysel',
 'psk',
 'rsa',
 'ikesel',
 'ike',
 'espsel',
 'esp',
 'pfs',
 'keymg',
 'keytm',
 'satm',
 'dpd',
 'dpddelay',
 'dpdtmout',
 'dpdact',
 'auto',
 'rekey'
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_vpn;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_vpn{"$k"};
		$id->{"$k"} = $item_def_vpn{"$k"};
	}

	for (my $i = 1; $i <= $list_count; $i++) {
		my @Key = keys %item_vpnset;

		foreach my $k (@Key) {
			$it->{"$k$i"} = $item_vpnset{"$k"}."$i";
			$id->{"$k$i"} = $item_def_vpnset{"$k"};
		}
	}
}

sub get_item_vpnsetn {
#	my @dt = @_;
	my @dt = ();
	foreach my $k (@item_vpnsetn) {
		push(@dt, $k);
	}
	return @dt;
}

sub get_list_count {
	return $list_count;
}

sub get_conf_file {
	return $conf_file;
}

sub get_setkey_tflag {
	return $setkey_tflag;
}

sub get_rsapubkey_file {
	return $rsapubkey_file;
}

sub get_subnetaddress {
	my ($adr, $zero) = @_;

	if (length $adr) {
		my @sub = split(/\//,  $adr, 2);
		if (defined $sub[0] && defined $sub[1]){
			if(&hyper::get_ipaddress($sub[0], 1) eq "") {
				return undef;
			}
			if(&hyper::get_submask($sub[1], 1) eq "") {
				if (&hyper::checknumstring($sub[1]) == 0) {
					return undef;
				}
				if (($sub[1] < 0) || ($sub[1] > 32)) {
					return undef;
				}
			}
			return 1;
			}
		return undef;
	}
	return $zero; # NULL
}

1;
