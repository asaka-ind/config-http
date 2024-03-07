package network;

require "/home/httpd/cgi-bin/hyper.pl";

%item_network = (
 'ipadr1'       => "ipadr1",
 'subnetadr1'   => "subnetadr1",
 'configport'   => "configport",
 'wanconfig'    => "wanconfig",
);

%item_def_network = (
 'ipadr1'       => "192.168.1.1",
 'subnetadr1'   => "255.255.255.0",
 'configport'   => "80",
 'wanconfig'    => "ACCEPT",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_network;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_network{"$k"};
		$id->{"$k"} = $item_def_network{"$k"};
	}
}
1;
