package rssetup;

require "/home/httpd/cgi-bin/hyper.pl";

%item_rssetup = (
 'rsprotocol'     => "rsprotocol",
 'rslocalport'    => "rslocalport",
 'rsremoteip1'    => "rsremoteip1",
 'rsremoteip2'    => "rsremoteip2",
 'rsremotechange' => "rsremotechange",
 'rsremoteport'   => "rsremoteport",
 'rstcpreconnect' => "rstcpreconnect",
 'rstcpclosetime' => "rstcpclosetime",
 'rsrecvtime'     => "rsrecvtime",
 'rsbufclear'     => "rsbufclear",
 'rsflow'         => "rsflow",
 'rsproconmode'   => "rsproconmode",
 'rsmaxrecvsize'  => "rsmaxrecvsize",
 'rsudpsenddelay' => "rsudpsenddelay",
 'rsspeed'        => "rsspeed",
 'rscharacterlen' => "rscharacterlen",
 'rsparitybit'    => "rsparitybit",
 'rsstopbit'      => "rsstopbit",
);
                 
%item_def_rssetup = (
 'rsprotocol'     => "0",
 'rslocalport'    => "1111",
 'rsremoteip1'    => "0.0.0.0",
 'rsremoteip2'    => "0.0.0.0",
 'rsremotechange' => "4",
 'rsremoteport'   => "1111",
 'rstcpreconnect' => "4",
 'rstcpclosetime' => "60",
 'rsrecvtime'     => "10",
 'rsbufclear'     => "0",
 'rsflow'         => "0",
 'rsproconmode'   => "0",
 'rsmaxrecvsize'  => "1024",
 'rsudpsenddelay' => "100",
 'rsspeed'        => "19200",
 'rscharacterlen' => "8",
 'rsparitybit'    => "0",
 'rsstopbit'      => "1",
);
                  
sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_rssetup;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_rssetup{"$k"};
		$id->{"$k"} = $item_def_rssetup{"$k"};
	}
}
1;
