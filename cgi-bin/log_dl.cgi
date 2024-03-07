#!/usr/bin/perl -w

open(IN, "</home/log/logno");
$finum = <IN>;
close(IN);

$files[0] = "/home/log/logfile$finum";
$j=1;
for($curnum = $finum-1; $curnum != $finum; $curnum--)
{
	if( $curnum == -1){
	if( $finum == 9){
		last;
	}else{
 		$curnum = 9;
	}
	}
	if( -f "/home/log/logfile$curnum"){
		$files[$j] = "/home/log/logfile$curnum ";
		$j++;
	}else{
		last;
	}
}


@files = reverse(@files);

#open(FH, "ls -r /etc/log/logfile? |");
#my @files = <FH>;
#close(FH);

my $now_time = `date '+%d%H%M'`;
chomp($now_time);
my $default_name = "log_$now_time.csv";
print "Content-type: application/download\n";
print "Content-disposition: attachment; filename=\"$default_name\"\n\n";
foreach my $file (@files){
	chomp($file);
	#print "file = $file \n";
	open(LOG,"$file");
	while(my $line = <LOG>){
		chomp($line);
		print "$line\r\n";
	}
	close(LOG);
}

