#!/usr/bin/perl -w
use Time::Local;
use strict;

my $now = time();
my $threshold = $now - 604800; # days in seconds (86400 = 1 day, 604800 = 7 days, 2592000 = 30 days, etc.)
my $recipient = 'thartmann@illumina.com';
my $mailx = "/bin/mailx";
my $hostname = `hostname`;

my @qstat = `qstat -u '*'`;
chomp @qstat;

#  326267 0.60500 QLOGIN     ichorny      r     01/22/2013 09:47:59 devel.q@ussd-prd-lncn-2-7.loca    12
foreach (@qstat) {
  if(/(\d+).*QLOGIN\s+(\w+)\s+\w\s+(\d\d)\/(\d\d)\/(\d\d\d\d)/){
    my ($jobid, $user) = ($1, $2);
    my ($month, $day, $year) = ($3, $4, $5);
    $month = $month - 1;
    my $submit_time = timelocal(0,0,0,$day,$month,$year);
    if ($submit_time < $threshold){
      $month = $month + 1;
      #my $body = "You have an open QLOGIN session with jobid $jobid on cluster $hostname that was submitted on $month/$day/$year. Please try to limit your QLOGIN sessions to 7 days or less\n";
      my $body = "$user $jobid $month/$day/$year\n";
      print $body;
      #open my $pipe, '|-',$mailx,'-s',"QLOGIN test",$recipient or die "can't open pipe to mailx: $!\n";
      #print $pipe $body;
      #close $pipe;
    }
  }
}

