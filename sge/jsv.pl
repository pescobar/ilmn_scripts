#!/usr/bin/perl
use strict;
use warnings;
no warnings qw/uninitialized/;
use Switch;

use Env qw(SGE_ROOT);
use lib "$SGE_ROOT/util/resources/jsv";
use JSV qw( :ALL );

my $debug = 1; # true: log and reject

jsv_on_start(sub {
  jsv_send_env();
});

jsv_on_verify(sub {
  my %params = jsv_get_param_hash();

  jsv_show_params() if $debug;

  # first remove all requests for specific queues - we'll handle queue assignment later
  if (exists $params{q_hard}) {
    jsv_set_param('q_hard', '');
    jsv_log_info("Removed requested queue") if $debug;
  }
  if (exists $params{q_soft}) {
    jsv_set_param('q_soft', '');
    jsv_log_info("Removed requested queue") if $debug;
  }
  if (! ($params{q_hard} || $params{q_soft})){
    jsv_log_info("Job without queue request submitted") if $debug;
  }

  # all qlogins also go to the devel.q but we also strip out any -pe requests
  if ($params{CLIENT} eq "qlogin") {
    if (exists $params{pe_name}){
      jsv_set_param('pe_min', '');
      jsv_set_param('pe_max', '');
      jsv_set_param('pe_name', '');
      jsv_log_info("parallel qlogin squashed") if $debug;
    }
    jsv_log_info("qlogin directed to devel.q") if $debug;
    jsv_set_param('q_hard', 'devel.q');
    jsv_show_params() if $debug; # show params again to see modifications
    jsv_reject() if $debug;
    jsv_accept();
  }

  # TODO: do we need to select on pe name? or just # slots?
  # should only have make, orte, and threaded (fill_up, fill_node need to go away!)
  #    make is $round_robin - slots are dispersed as widely as possible
  #    orte is $fill_up - slots are packed onto one node before moving on to another node
  #    threaded is $pe_slots - jobs will run on one node only
  if (exists $params{pe_name}){
    switch ($params{pe_name}){
      case "make"       { jsv_set_param('pe_name', 'threaded'); jsv_log_info("$params{pe_name} specified") if $debug; }
      case "threaded"   { jsv_set_param('pe_name', 'threaded'); jsv_log_info("$params{pe_name} specified") if $debug; }
      case "orte"       { jsv_set_param('pe_name', 'threaded'); jsv_log_info("$params{pe_name} specified") if $debug; }
    }

    my $slots = $params{pe_min};
    if($slots > 11){
      jsv_set_param('q_hard', 'devel.q');
      jsv_set_param('l_hard', 'exclusive');
      jsv_log_info("big parallel job redirected") if $debug;
      jsv_show_params() if $debug; # show params again to see modifications
      jsv_reject() if $debug;
      jsv_accept();
    }else{
      jsv_set_param('q_hard', 'sqa.q');
      jsv_log_info("small parallel job redirected") if $debug;
      jsv_show_params() if $debug; # show params again to see modifications
      jsv_reject() if $debug;
      jsv_accept();
    }
  }

   # log exclusive job requests for tracking
  if ($params{l_hard}) {
    if ($params{l_hard}{exclusive}) {
      jsv_log_warning("exclusive mode detected for $params{CMDNAME} job submitted by $params{USER}");
    }
  }

  jsv_show_params() if $debug; # show params again to see modifications

  if ($debug) {
    jsv_reject();
    #jsv_accept();
  } else {
    jsv_accept();
  }
  return;
}); 

jsv_main();
