#!/usr/bin/perl
use strict;
use warnings;
no warnings qw/uninitialized/;

use Env qw(SGE_ROOT);
use lib "$SGE_ROOT/util/resources/jsv";
use JSV qw( :ALL );

my $debug = 1; # true: log and reject

jsv_on_start(sub {
  jsv_send_env();
});

jsv_on_verify(sub {
  my %params = jsv_get_param_hash();

  jsv_show_params() if($debug);

  # first remove all requests for specific queues - we'll handle queue assignment later
  if (exists $params{q_hard}) {
    jsv_set_param('q_hard', '');
    jsv_log_info("Removed requested queue") if($debug);
  }
  if (exists $params{q_soft}) {
    jsv_set_param('q_soft', '');
    jsv_log_info("Removed requested queue") if($debug);
  }

  if ($params{pe_name}) {
    jsv_set_param('q_hard', 'devel.q');
    jsv_log_info("Parallel job") if($debug);
  } else {
    jsv_set_param('q_hard', 'sqa.q');
    jsv_log_info("Single slot") if($debug);
  }

  # all qlogins also go to the devel.q but we also strip out any -pe requests
  if ($params{CLIENT} =~ /qlogin/) {
    jsv_set_param('pe_min', '');
    jsv_set_param('pe_max', '');
    jsv_set_param('pe_name', '');
    jsv_set_param('q_hard', 'devel.q');
    jsv_log_info("qlogin redirected with 1 job slot") if($debug);
  }

  jsv_show_params() if($debug); # show params again to see modifications

  if ($debug) {
    #jsv_reject();
    jsv_accept();
  } else {
    jsv_accept();
  }
  return;
}); 

jsv_main();
