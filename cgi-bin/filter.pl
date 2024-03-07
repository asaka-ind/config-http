package filter;

require "/home/httpd/cgi-bin/hyper.pl";

$list_count = 50;

%item_filter = (
 'filtuse'     => "filtuse",
 'filtset'     => "filtset",
 'filtsel'     => "filtsel",
 'filtproto'   => "filtproto",
 'filtwanip'   => "filtwanip",
 'filtwanmask' => "filtwanmask",
 'filtwanport' => "filtwanport",
 'filtlanip'   => "filtlanip",
 'filtlanmask' => "filtlanmask",
 'filtlanport' => "filtlanport",
);

%item_def_filter = (
 'filtuse'     => "",
 'filtset'     => "",
 'filtsel'     => "",
 'filtproto'   => "",
 'filtwanip'   => "",
 'filtwanmask' => "",
 'filtwanport' => "",
 'filtlanip'   => "",
 'filtlanmask' => "",
 'filtlanport' => "",
);

@opt_filtsel   = ("������","WAN����LAN","LAN����WAN");
@opt_filtproto = ("TCP&amp;UDP", "TCP", "UDP", "ICMP", "����");
@opt_filtset   = ("����", "����");
@opt_filtuse   = ("̵��", "ͭ��");

sub make_list {
	my ($it, $id) = @_;

	for (my $i = 1; $i <= $list_count; $i++) {
		my @Key = keys %item_filter;

		foreach my $k (@Key) {
			$it->{"$k$i"} = $item_filter{"$k"}."$i";
			$id->{"$k$i"} = $item_def_filter{"$k"};
		}
	}
}
1;
