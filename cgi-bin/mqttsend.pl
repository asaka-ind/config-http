package mqttsend;

require "/home/httpd/cgi-bin/hyper.pl";

%item_mqttsend = (
 'log_onoff'        => "log_onoff",
 'logbuf_massive'   => "logbuf_massive",
 'logbuf_max'       => "logbuf_max",
 'logbuf_line'      => "logbuf_line",
 'status'           => "status",
 'status_time'      => "status_time",
 'databyte'         => "databyte",
 'latency'          => "latency",
 'latency_sel'      => "latency_sel",
 'ant'              => "ant",
 'timediv'          => "timediv",
);

%item_def_mqttsend = (
 'log_onoff'        => "0",
 'logbuf_massive'   => "0",
 'logbuf_max'       => "20",
 'logbuf_line'      => "0",
 'status'           => "0",
 'status_time'      => "",
 'databyte'         => "0",
 'latency'          => "0",
 'latency_sel'      => "1",
 'ant'              => "0",
 'timediv'          => "0",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_mqttsend;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_mqttsend{"$k"};
		$id->{"$k"} = $item_def_mqttsend{"$k"};
	}
}
1;
