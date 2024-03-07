#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";
require "/home/httpd/cgi-bin/filter.pl";

%item_list = ();
%item_def = ();

my $commandline = "";
my %items = ();
my $setting = "";
my $err_item ="";
my $section = "filtersetup";

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Status: 302 Moved\n";
	print "Location: ./general.cgi\n\n";
	#exit;
}

&filter::make_list(\%item_list, \%item_def);
%items = &hyper::get_section("filtersetup", "" ,\%item_list, \%item_def);
my @ddd = keys %items;

my $table = &make_table(%items);

sub make_table {
	my %items = @_;
	my $i;
	my $upbtn;

	my $p =<<"THCAPTION";
    <TR>
      <TH nowrap>ͥ����</TH>
      <TH nowrap>ư��</TH>
      <TH nowrap>�ե��륿����</TH>
      <TH nowrap>���</TH>
    </TR>
THCAPTION
	my $add = 1;
	my @color = ("bgcolor=#d0d0d0", "bgcolor=#e0e0e0");
	for ($i = 1; $i <= $filter::list_count; $i++) {
		if (length $items{"filtuse$i"}) {
			my %it = (
			 'filtuse'     => $filter::opt_filtuse[$items{"filtuse$i"}],
			 'filtset'     => $filter::opt_filtset[$items{"filtset$i"}],
			 'filtsel'     => $filter::opt_filtsel[$items{"filtsel$i"}],
			 'filtproto'   => $filter::opt_filtproto[$items{"filtproto$i"}],
			 'filtwanip'   => $items{"filtwanip$i"},
			 'filtwanmask' => $items{"filtwanmask$i"},
			 'filtwanport' => $items{"filtwanport$i"},
			 'filtlanip'   => $items{"filtlanip$i"},
			 'filtlanmask' => $items{"filtlanmask$i"},
			 'filtlanport' => $items{"filtlanport$i"},
			);
			#NULL�ο�����
			$it{'filtwanip'}   = "---.---.---.---" unless length $it{'filtwanip'};
			$it{'filtwanmask'} = "---.---.---.---" unless length $it{'filtwanmask'};
			$it{'filtwanport'} = "-----" unless length $it{'filtwanport'};

			$it{'filtlanip'}   = "---.---.---.---" unless length $it{'filtlanip'};
			$it{'filtlanmask'} = "---.---.---.---" unless length $it{'filtlanmask'};
			$it{'filtlanport'} = "-----" unless length $it{'filtlanport'};

			if ($i == 1) {
				$upbtn = '&nbsp;';
			}
			else {
				$upbtn = "<INPUT type=\"submit\" name=\"btnUp$i\" value=\"���\">";
			}
			$p .=<<"TDHTML";
    <TR>
      <TD align="center" valign="middle" $color[$i%2] nowrap>$i</TD>
      <TD align="center" valign="middle" $color[$i%2] nowrap>$it{filtuse}</TD>
      <TD $color[$i%2] nowrap><TABLE border="1" frame="void" cellspacing="1">
          <TBODY>
            <TR>
              <TD width="80"  nowrap><FONT SIZE=-1>���ꡧ</FONT></TD>
              <TD width="200" nowrap><FONT SIZE=-1>�ѥ��åȤθ�����&nbsp;$it{filtsel}&nbsp;</FONT></TD>
              <TD width="200" nowrap><FONT SIZE=-1>�ץ�ȥ��롧&nbsp;$it{filtproto}&nbsp;</FONT></TD>
              <TD width="80" nowrap><FONT SIZE=-1>�̿���&nbsp;$it{filtset}&nbsp;</FONT></TD>
            </TR>
            <TR>
              <TD nowrap><FONT SIZE=-1>WAN¦��</TD>
              <TD nowrap><FONT SIZE=-1>IP���ɥ쥹��&nbsp;$it{filtwanip}&nbsp;</FONT></TD>
              <TD nowrap><FONT SIZE=-1>���֥ͥåȥޥ�����&nbsp;$it{filtwanmask}&nbsp;</FONT></TD>
              <TD nowrap><FONT SIZE=-1>�ݡ��ȡ�&nbsp;$it{filtwanport}</FONT></TD>
            </TR>
            <TR>
              <TD nowrap><FONT SIZE=-1>LAN¦��</FONT></TD>
              <TD nowrap><FONT SIZE=-1>IP���ɥ쥹��&nbsp;$it{filtlanip}&nbsp;</FONT></TD>
              <TD nowrap><FONT SIZE=-1>���֥ͥåȥޥ�����&nbsp;$it{filtlanmask}&nbsp;</FONT></TD>
              <TD nowrap><FONT SIZE=-1>�ݡ��ȡ�&nbsp;$it{filtlanport}&nbsp;</FONT></TD>
            </TR>
        </TBODY>
        </TABLE>
      </TD>
      <TD $color[$i%2]><TABLE border="0" cellspacing="0" cellpadding="1">
          <TBODY>
            <TR>
              <TD><INPUT type="submit" name="btnModify$i" value="����"></TD>
            </TR>
            <TR>
              <TD><INPUT type="submit" name="btnDelete$i" value="���"></TD>
            </TR>
            <TR>
              <TD>$upbtn</TD>
            </TR>
          </TBODY>
          </TABLE>
      </TD>
    </TR>
TDHTML
		}
		else {
			my $btnline;
			if ($add) {
				$btnline = "<INPUT type=\"submit\" name=\"btnModify$i\" value=\"�ɲ�\">";
				$add = 0;
			}
			else {
				$btnline = "&nbsp;";
			}

			$p .=<<"TDNOHTML";
    <TR>
      <TD align="center" valign="middle">$i</TD>
      <TD align="center" valign="middle">̵��</TD>
      <TD align="center" valign="middle">����ʤ�</TD>
      <TD>$btnline</TD>
    </TR>
TDNOHTML
		}
	}
	return $p;
}


print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 10.0.2.0 for Windows">
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK href="../html/hpbsite.css" rel="stylesheet" type="text/css">
<TITLE></TITLE>
</HEAD>
<BODY bgcolor="#cccccc">
<H2>�ե��륿����</H2>
<FORM method="POST" action="./filtersetup.cgi">
<INPUT type="hidden" name="type" value="view">
<TABLE  border="1" cellpadding=2>
  <TBODY>
  $table
  </TBODY>
</TABLE>
</FORM>
</BODY>
</HTML>
EOFHTML
