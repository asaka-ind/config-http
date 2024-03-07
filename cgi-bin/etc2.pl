package etc2;

require "/home/httpd/cgi-bin/hyper.pl";

%item_etc2 = (
 'dnsfwd_onoff'      => "dnsfwd_onoff",
 'dscpclear_onoff'      => "dscpclear_onoff",
 'antenna'              => "antenna",
 'antenna_time'         => "antenna_time",
 'modelog'              => "modelog",
 'modelog_time'         => "modelog_time",
);

%item_def_etc2 = (
 'dnsfwd_onoff'      => "1",
 'dscpclear_onoff'      => "0",
 'antenna'              => "0",
 'antenna_time'         => "",
 'modelog'              => "0",
 'modelog_time'         => "",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_etc2;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_etc2{"$k"};
		$id->{"$k"} = $item_def_etc2{"$k"};
	}
}
1;
