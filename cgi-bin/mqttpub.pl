package mqttpub;

require "/home/httpd/cgi-bin/hyper.pl";

%item_mqttpub = (
 'pubon'            => "pubon",
 'protocol'         => "protocol",
 'authon'           => "authon",
 'pubuser'          => "pubuser",
 'pubpasswd'        => "pubpasswd",
 'brokerip'         => "brokerip",
 'qos'              => "qos",
 'topic'            => "topic",
 'retain'           => "retain",
 'pubid'            => "pubid",
 'mqttport'         => "mqttport",
 'keepalive'        => "keepalive",
 'clientcrt'        => "clientcrt",
 'willon'           => "willon",
 'willtopic'        => "willtopic",
 'willmessage'      => "willmessage",
 'willqos'          => "willqos",
 'willretain'       => "willretain",
 'mqttver'          => "mqttver",
 'tlsver'           => "tlsver",
);

%item_def_mqttpub = (
 'pubon'            => "0",
 'protocol'         => "0",
 'authon'           => "0",
 'pubuser'          => "",
 'pubpasswd'        => "",
 'brokerip'         => "",
 'qos'              => "0",
 'topic'            => "",
 'retain'           => "0",
 'pubid'            => "",
 'mqttport'         => "8883",
 'keepalive'        => "600",
 'clientcrt'        => "0",
 'willon'           => "0",
 'willtopic'        => "",
 'willmessage'      => "",
 'willqos'          => "0",
 'willretain'       => "0",
 'mqttver'          => "1",
 'tlsver'           => "2",
);

sub make_list {
	my ($it, $id) = @_;

	my @Key = keys %item_mqttpub;

	foreach my $k (@Key) {
		$it->{"$k"} = $item_mqttpub{"$k"};
		$id->{"$k"} = $item_def_mqttpub{"$k"};
	}
}
1;
