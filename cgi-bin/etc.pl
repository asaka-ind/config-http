package etc;

require "/home/httpd/cgi-bin/hyper.pl";

%item_etc = (
 'icmp'      => "icmp",
 'virtserve' => "virtserve",
 'virtip'    => "virtip",
 'reboot'    => "reboot",
 'reboot_time'    => "reboot_time",
 'pingcheck'    => "pingcheck",
 'ipdomain'    => "ipdomain",
 'pingip'    => "pingip",
 'sleep_time'    => "sleep_time",
 'errorcount'    => "errorcount",
 'pingcheck2'    => "pingcheck2",
 'pingip2'    => "pingip2",
 'sleep_time2'    => "sleep_time2",
 'errorcount2'    => "errorcount2",
 'pingcheck4'    => "pingcheck4",
 'pingip4'    => "pingip4",
 'sleep_time4'    => "sleep_time4",
 'errorcount4'    => "errorcount4",
 'pingcheck3'    => "pingcheck3",
 'pingip3'    => "pingip3",
 'pinglocalip3'    => "pinglocalip3",
 'sleep_time3'    => "sleep_time3",
 'errorcount3'    => "errorcount3",
);

%item_def_etc = (
 'icmp'      => "1",
 'virtserve' => "0",
 'virtip'    => "",
 'reboot'    => "0",
 'reboot_time'    => "86400",
 'pingcheck'    => "0",
 'ipdomain'    => "0",
 'pingip'    => "",
 'sleep_time'    => "60",
 'errorcount'    => "3",
 'pingcheck2'    => "0",
 'pingip2'    => "",
 'sleep_time2'    => "60",
 'errorcount2'    => "3",
 'pingcheck4'    => "0",
 'pingip4'    => "",
 'sleep_time4'    => "60",
 'errorcount4'    => "3",
 'pingcheck3'    => "0",
 'pingip3'    => "",
 'pinglocalip3'    => "",
 'sleep_time3'    => "60",
 'errorcount3'    => "3",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_etc;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_etc{"$k"};
		$id->{"$k"} = $item_def_etc{"$k"};
	}
}
1;
