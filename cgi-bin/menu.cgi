#!/usr/bin/perl -w
#use CGI::Carp qw(fatalsToBrowser);
#use strict;
#use warnings;

require "/home/httpd/cgi-bin/hyper.pl";

#-------------------
# 設定メニュー表示
#-------------------

my $commandline = "";
my $login_user = "";
my $contents = "";

sub HtmlTopJs{
  return <<END_OF_TEXT;
<!DOCTYPE HTML>
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE></TITLE>
<LINK href="./../html/status.css" rel="stylesheet" type="text/css">
<script type="text/javascript">
<!--
function showPlagin(idno){
    pc = ('PlagClose' + (idno));
    po = ('PlagOpen' + (idno));
    if( document.getElementById(pc).style.display == "none" ){
        document.getElementById(pc).style.display = "block";
        document.getElementById(po).style.display = "none";
    }else{
        document.getElementById(pc).style.display = "none";
        document.getElementById(po).style.display = "block";
    }
}
-->
</script>
</HEAD>
END_OF_TEXT
}

#BODY_TOP
sub HtmlBody{
  return <<END_OF_TEXT;
<BODY>
<CENTER>
END_OF_TEXT
}

#BOTTOM
sub HtmlBottom{
  return <<END_OF_TEXT;
</CENTER>
</BODY>
</HTML>
END_OF_TEXT
}

#LINK
sub HtmlLink{
  my($name, $href) = @_; # name:項目名称, href:URL
  return <<END_OF_TEXT;
<TR><TD width="220"><FONT color="#0000ff"><A href="$href" target="right">$name</A></FONT></TD></TR>
END_OF_TEXT
}

#折りたたみ
sub HtmlFold{
  my ($id,$name,$contents) = @_;
  my $outtag = "";
$outtag = '<div id="PlagOpen'.$id.'">';
$outtag .= '<p></p>';
$outtag .= '<TABLE>';
$outtag .= '<tr><th width="220px"><a href="#" onclick="showPlagin('.$id.');return false;">'.$name.'▼</a></th></tr>';
$outtag .= '</TABLE>';
$outtag .= '</div>';

$outtag .= '<div id="PlagClose'.$id.'" style="display: none">';
$outtag .= '<p></p>';
$outtag .= '<TABLE>';
$outtag .= '<tr><th width="220px"><a href="#" onclick="showPlagin('.$id.');return false;">'.$name.'▽</a></th></tr>';
$outtag .= $contents;
$outtag .= '</TABLE>';
$outtag .= '</div>';
return $outtag;
}

print "Content-Type:text/html\r\n\r\n";
print &HtmlTopJs;
$login_user = &hyper::get_logincheck();

print &HtmlBody;

# 基本設定
$contents = &HtmlLink("本体設定","general.cgi");
$contents .= &HtmlLink("ネットワーク","network.cgi");
$contents .= &HtmlLink("WAN設定","wansetup.cgi");
#$contents .= &HtmlLink("SMS着信設定","smssetup.cgi");
print &HtmlFold(1,"基本設定", $contents);

# NAT・セキュリティ
$contents = &HtmlLink("静的NAT設定","snatsetup.cgi");
$contents .= &HtmlLink("VPN設定","vpn.cgi");
$contents .= &HtmlLink("フィルタ設定","filterview.cgi");
print &HtmlFold(2,"NAT・セキュリティ", $contents);

# ルータ機能
$contents = &HtmlLink("ダイナミックDNS","ddnssetup.cgi");
$contents .= &HtmlLink("DHCP設定","dhcpsetup.cgi");
$contents .= &HtmlLink("NTP設定","ntpsetup.cgi");
print &HtmlFold(3,"ルータ機能", $contents);

# RS232Cプロコン
$contents = &HtmlLink("RS-232Cプロトコル変換","rssetup.cgi");
$contents .= &HtmlLink("メッセージ&信号線","rsstatussetup.cgi");
print &HtmlFold(4,"プロトコル変換", $contents);

# その他機能
$contents = &HtmlLink("その他設定","etcsetup.cgi");
$contents .= &HtmlLink("その他設定２","etcsetup2.cgi");
print &HtmlFold(5,"その他機能", $contents);

# IOT
$contents = &HtmlLink("MQTTパブリッシャー","mqttpubsetup.cgi");
$contents .= &HtmlLink("通知内容","mqttsendsetup.cgi");
$contents .= &HtmlLink("CA認証局","cacrtfile.cgi");
$contents .= &HtmlLink("クライアント証明書","clicrtfile.cgi");
$contents .= &HtmlLink("クライアント秘密鍵","privatefile.cgi");
#$contents .= &HtmlLink("MQTTブローカー","mqttbrsetup.cgi");
print &HtmlFold(6,"IOT", $contents);

# 設定保存
$contents = &HtmlLink("設定保存","setup.cgi");
$contents .= &HtmlLink("初期化","init.cgi");
$contents .= &HtmlLink("全設定ファイル","configfile.cgi");
print &HtmlFold(7,"設定保存", $contents);

# メンテナンス
$contents = &HtmlLink("動作ログ","log_get.cgi");
$contents .= &HtmlLink("パスワード変更","password.cgi");
$contents .= &HtmlLink("再起動","restart.cgi");
#$contents .= &HtmlLink("モジュール更新","fota.cgi");
$contents .= &HtmlLink("バージョンアップ","versionup.cgi");
print &HtmlFold(8,"メンテナンス", $contents);

print '<P><A href="http://www.i-netd.co.jp/" target="_parent"><IMG src="../img/logo2.jpg" width="139" height="23" border="0" align="middle" alt="株式会社 iND"></A></P>';

print &HtmlBottom;
