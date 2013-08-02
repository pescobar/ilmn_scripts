#!/usr/bin/perl
use strict;
use warnings;
no warnings qw/uninitialized/;

use Env qw(SGE_ROOT);
use lib "$SGE_ROOT/util/resources/jsv";
use JSV qw( :DEFAULT jsv_send_env jsv_log_info );

jsv_on_start(sub {
   jsv_send_env();
});

jsv_on_verify(sub {
   my %params = jsv_get_param_hash();
   my $do_correct = 0;
   my $do_wait = 0;

   # parallel jobs should be multiple of 16
   if ($params{pe_name}) {
      my $slots = $params{pe_min};
      if (($slots % 16) != 0) {
         jsv_reject('Parallel job does not request a multiple of 16 slots');
         return;
      }
   }

   # if any queue is specified nuke that resource request
   if (exists $params{q_hard}) {
      jsv_set_param('q_hard', '');
   }
   if (exists $params{q_soft}) {
      jsv_set_param('q_soft', '');
   }

   if ($do_wait) {
      jsv_reject_wait('Job is rejected. It might be submitted later.');
   } elsif ($do_correct) {
      jsv_correct('Job was modified before it was accepted');
   } else {
      jsv_accept('Job is accepted');
   }
}); 

jsv_main();

