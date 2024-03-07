package snat;

require "/home/httpd/cgi-bin/hyper.pl";

$list_count = 50;

%item_snatsetup = (
 'snatwanport' => "snatwanport",
 'snatlanip'   => "snatlanip",
 'snatlanport' => "snatlanport",
);

%item_def_snatsetup = (
 'snatwanport' => "",
 'snatlanip'   => "",
 'snatlanport' => "",
);

sub make_list {
	my ($it, $id) = @_;

	for (my $i = 1; $i <= $list_count; $i++) {
		my @Key = keys %item_snatsetup;

		foreach my $k (@Key) {
			$it->{"$k$i"} = $item_snatsetup{"$k"}."$i";
			$id->{"$k$i"} = $item_def_snatsetup{"$k"};
		}
	}
}
1;
