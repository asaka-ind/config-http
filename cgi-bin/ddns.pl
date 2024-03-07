package ddns;

require "/home/httpd/cgi-bin/hyper.pl";

%item_ddns = (
 'ddns_onoff'   => "ddns_onoff",
 'ddnsserver'   => "ddnsserver",
 'ddnsname'     => "ddnsname",
 'ddnsuser'     => "ddnsuser",
 'ddnspasswd'   => "ddnspasswd",
);

%item_def_ddns = (
 'ddns_onoff'   => "0",
 'ddnsserver'   => "1",
 'ddnsname'     => "",
 'ddnsuser'     => "",
 'ddnspasswd'   => "",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_ddns;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_ddns{"$k"};
		$id->{"$k"} = $item_def_ddns{"$k"};
	}
}
1;
