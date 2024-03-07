package wan;

require "/home/httpd/cgi-bin/hyper.pl";

%item_wan = (
 'authtype'     => "authtype",
 'pppuser'      => "pppuser",
 'ppppasswd'    => "ppppasswd",
 'dhcpdns1'     => "dhcpdns1",
 'dhcpdns2'     => "dhcpdns2",
 'wanip'        => "wanip",
 'carrier_id'   => "carrier_id",
 'remoteip'     => "remoteip",
 'idle_time'    => "idle_time",
 'wan_mode'	=> "wan_mode",
 'wancheck'     => "wancheck",
 'lcpecho'	=> "lcpecho",
 'apn'		=> "apn",
 'pdp'		=> "pdp",
 'dialicmp'     => "dialicmp",
 'dialdns'      => "dialdns",
 'connect'      => "connect",
 'keeppacket'   => "keeppacket",
 'connecttime'  => "connecttime",
 'dnscheck'     => "dnscheck",
);

%item_def_wan = (
 'authtype'     => "2",
 'pppuser'      => "",
 'ppppasswd'    => "",
 'dhcpdns1'     => "",
 'dhcpdns2'     => "",
 'carrier_id'   => "1",
 'wanip'        => "",
 'remoteip'        => "",
 'idle_time'    => "180",
 'wan_mode'     => "0",
 'wancheck'     => "0",
 'lcpecho'	=> "0",
 'apn'          => "mopera.flat.foma.ne.jp",
 'pdp'          => "IP",
 'dialicmp'     => "1",
 'dialdns'      => "1",
 'connect'      => "1",
 'keeppacket'   => "0",
 'connecttime'  => "0",
 'dnscheck'     => "0",
);

%item_list = (%item_wan);

%item_def = (%item_def_wan);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_wan;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_wan{"$k"};
		$id->{"$k"} = $item_def_wan{"$k"};
	}
}
1;
