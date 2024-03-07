package ntp;

require "/home/httpd/cgi-bin/hyper.pl";

%item_ntp = (
 'ntp_onoff'      => "ntp_onoff",
 'ntpserver'      => "ntpserver",
 'reboot1_onoff'    => "reboot1_onoff",
 'reboot2_onoff'    => "reboot2_onoff",
 'month1'	    => "month1",
 'day1'		    => "day1",
 'hour1'	    => "hour1",
 'minute1'	    => "minute1",
 'week1'	    => "week1",
 'month2'	    => "month2",
 'day2'		    => "day2",
 'hour2'	    => "hour2",
 'minute2'	    => "minute2",
 'week2'	    => "week2",
);

%item_def_ntp = (
 'ntp_onoff'      => "1",
 'ntpserver'      => "ntp3.jst.mfeed.ad.jp",
 'reboot1_onoff'    => "0",
 'reboot2_onoff'    => "0",
 'month1'	    => "*",
 'day1'		    => "*",
 'hour1'	    => "*",
 'minute1'	    => "59",
 'week1'	    => "*",
 'month2'	    => "*",
 'day2'		    => "*",
 'hour2'	    => "*",
 'minute2'	    => "59",
 'week2'	    => "*",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_ntp;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_ntp{"$k"};
		$id->{"$k"} = $item_def_ntp{"$k"};
	}
}
1;
