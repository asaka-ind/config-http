#!/usr/bin/perl -w

require "/home/httpd/cgi-bin/hyper.pl";

my $commandline = "";

if (!&hyper::get_logincheck()) {
# admin�Ǥʤ��ʤ�TOP���᤹
	print "Location: ./general.cgi\n\n";
}

&hyper::get_args($commandline);			# ���������ؿ�
#$commandline = "btnInit=1";
if ($commandline) {
	$commandline = &hyper::url_decode($commandline);
	$setting = &hyper::get_param("btnInit", $commandline);
}

if ($setting ne "") {
#�ǥե��������ե饰��Ω�Ƥ�
	my $flag = &hyper::get_flag_file($hyper::flag_name{'default'});
	my @s = ("1");
	&hyper::writefile($flag, @s);

#�Ƶ�ư�ե饰��Ω�Ƥ�
	$flag = &hyper::get_flag_file($hyper::flag_name{'reboot'});
	&hyper::writefile($flag, @s);

print "Content-Type:text/html\r\n\r\n";
print <<EOFRESTART;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<STYLE TYPE="text/css">
<!--
#barBG { position:absolute;left:0px; font-size:4px;
         background-color:#d0d0d0; width:210px; height:32px;}
#bar   { position:absolute;left:5px; font-size:4px;
         background-color:#808080; width:0px;   height:22px; }
#progTitle {}
#progMsg {}
--></STYLE>
<SCRIPT Language="JavaScript">
<!--
// �ץ��쥹�С�ɽ��
per   = 0;			// �ѡ�����ơ���
total = 60;			// �ɤ߹���ȡ����������
//#barWidth = 200;	// �ץ��쥹�С��β���
function progressBar()
{
	wid = document.body.clientWidth;
	barWidth = wid-20;
	document.all["barBG"].style.width = barWidth+10;

	per++;
	w = (per / total) * barWidth;
	document.all["bar"].style.top   = document.all["barBG"].style.top+5;
	document.all["bar"].style.width = w;

	progTitle.innerText = "�������";
	var kaisu = total-per;
	progMsg.innerText = "��"+kaisu+"�ø�˺���³���Ƥ���������";

	if (per == total) setTimeout("hideProgressBar()",1000);
	else setTimeout('progressBar()',1000);
}
//�����÷вᤷ����ץ��쥹�С���õ�
function hideProgressBar()
{
	progTitle.innerText = "����³��ǽ�Ǥ���";
	document.all["progMsg"].style.visibility = "hidden";
	document.all["barBG"].style.visibility = "hidden";
}

// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc" onload="progressBar();">
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
<H2 align="center">�����</H2>
<CENTER>
<P><DIV ID="progTitle"></DIV></P>
<P><DIV ID="progMsg"></DIV></P>
</CENTER>
<P><DIV ID="barBG"><DIV ID="bar"></DIV></DIV></P>
</BODY>
</HTML>
EOFRESTART
}
else {
print "Content-Type:text/html\r\n\r\n";
print <<EOFHTML;


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="../html/hpbsite.css">
<META name="GENERATOR" content="IBM WebSphere Studio Homepage Builder Version 8.0.2.0 for Windows">
<TITLE></TITLE>
<SCRIPT Language="JavaScript">
<!--
function MCheck() {
	return window.confirm("����вٻ�������ᤷ�ޤ���������Ǥ�����");
}
// -->
</SCRIPT>
</HEAD>
<BODY bgcolor="#cccccc">
<noscript><p><font color="red">���Υڡ�����JavaScript����Ѥ��Ƥ��ޤ��� �����Ѥ�
�֥饦����JavaScript��̵���ˤʤäƤ��뤫��JavaScript���б����Ƥ��ޤ���JavaScript��ͭ���ˤ��뤫��JavaScript�����Ѳ�ǽ�ʥ֥饦���ǥ����������Ʋ�������</font></p></noscript>
<H2 align="center">�����</H2>
<FORM action="./init.cgi" method="post" onSubmit="return MCheck()">
<CENTER>�������Ԥ��ȡ����٤Ƥ����꤬����в��ͤ����ޤ���<BR>
<BR>
<INPUT type="submit" name="btnInit" value="������¹�"><BR>
</CENTER>
</FORM>
</BODY>
</HTML>
EOFHTML
}
