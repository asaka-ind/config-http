package sms;

require "/home/httpd/cgi-bin/hyper.pl";

%item_sms = (
 'sms'              => "sms",
 'slcpecho'         => "slcpecho",
 'smsforce'         => "smsforce",
 'smssend'          => "smssend",
 'smsauthtype'      => "smsauthtype",
 'spppuser'         => "spppuser",
 'sppppasswd'       => "sppppasswd",
 'sdhcpdns1'        => "sdhcpdns1",
 'sdhcpdns2'        => "sdhcpdns2",
 'swanip'           => "swanip",
 'sremoteip'        => "sremoteip",
 'sidle_time'       => "sidle_time",
 'sconnecttime'     => "sconnecttime",
 'sapn'             => "sapn",
 'spdp'             => "spdp",
 'sdnscheck'        => "sdnscheck",
 'sreceiveallow'    => "sreceiveallow",
 'sallownumber1'    => "sallownumber1",
 'sallownumber2'    => "sallownumber2",
 'sallownumber3'    => "sallownumber3",
 'sallownumber4'    => "sallownumber4",
 'sallownumber5'    => "sallownumber5",
 'sallownumber6'    => "sallownumber6",
 'sallownumber7'    => "sallownumber7",
 'sallownumber8'    => "sallownumber8",
 'sallownumber9'    => "sallownumber9",
 'sallownumber10'   => "sallownumber10",
);

%item_def_sms = (
 'sms'              => "0",
 'slcpecho'         => "1",
 'smsforce'         => "0",
 'smssend'          => "0",
 'smsauthtype'      => "2",
 'spppuser'         => "mopera",
 'sppppasswd'       => "pass",
 'sdhcpdns1'        => "220.159.212.200",
 'sdhcpdns2'        => "220.159.212.201",
 'swanip'           => "",
 'sremoteip'        => "",
 'sidle_time'       => "180",
 'sconnecttime'     => "600",
 'sapn'             => "mopera.net",
 'spdp'             => "IP",
 'sdnscheck'        => "0",
 'sreceiveallow'    => "0",
 'sallownumber1'    => "",
 'sallownumber2'    => "",
 'sallownumber3'    => "",
 'sallownumber4'    => "",
 'sallownumber5'    => "",
 'sallownumber6'    => "",
 'sallownumber7'    => "",
 'sallownumber8'    => "",
 'sallownumber9'    => "",
 'sallownumber10'   => "",
);

%item_list = (%item_sms);

%item_def = (%item_def_sms);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_sms;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_sms{"$k"};
		$id->{"$k"} = $item_def_sms{"$k"};
	}
}
1;
