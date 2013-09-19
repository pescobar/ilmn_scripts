#!/usr/bin/perl
use strict;
use warnings;
no warnings qw/uninitialized/;
use Switch;

use Env qw(SGE_ROOT);
use lib "$SGE_ROOT/util/resources/jsv";
use JSV qw( :ALL );

my $debug = 1; # true: verose logging and all jobs are rejected
my $mem_threshold = 128; # threshold for large memory jobs (GB)
my $slot_threshold = 12; # threshold for large parallel jobs (slots)
my $mem_multiplier = 4; # set h_vmem = $mem_multiplier * slots (GB) for jobs with no mem limit
my $qlogin_memory_limit = 4; # (GB)
my $qlogin_time_limit = 24; # (hours)
my @exclude = qw/sqa.q gpu.q/;

jsv_on_start(sub {
  jsv_send_env();
});

jsv_on_verify(sub {
  my %params = jsv_get_param_hash();

  if ($debug){
    jsv_log_info("--- INITIAL PARAMS ---");
    jsv_show_params();
  }

  ###########################################
  # Queues excluded from JSV processing
  ###########################################
  for(@exclude){
    if (jsv_sub_is_param('q_hard', $_)){
      # queue is excluded from JSV - submit job as is
      if ($debug) {
        jsv_log_info("--- CORRECTED PARAMS ---");
        jsv_show_params();
        jsv_reject();
      } else {
        jsv_accept();
      }
    }
  }
  ##################################################################################
  # Qlogin
  #   all qlogins go to the slice.q
  #   strip out any -pe requests and set hard run time and memory limits
  #   TODO: what about special queues like sqa, gpu, etc.? An exclude list maybe?
  ##################################################################################
  if ($params{CLIENT} eq "qlogin") {
    if (jsv_is_param('pe_name')){
      jsv_del_param('pe_name');
      jsv_del_param('pe_min');
      jsv_del_param('pe_max');
    }
    jsv_sub_del_param('l_hard', 'h_vmem') if (jsv_sub_is_param('l_hard','h_vmem'));
    jsv_sub_del_param('l_hard', 'h_rt') if (jsv_sub_is_param('l_hard','h_rt'));
    jsv_set_param('q_hard', 'slice.q');
    jsv_sub_add_param('l_hard', "h_rt=$qlogin_time_limit:0:0");
    jsv_sub_add_param('l_hard', "h_vmem=$qlogin_memory_limit" . "g");
    # we're done, correct and submit
    if ($debug) {
      jsv_log_info("--- CORRECTED PARAMS ---");
      jsv_show_params();
      jsv_reject();
    } else {
      jsv_correct();
    }
  }

  #########################################################################
  # Jobs with large memory requirements
  #########################################################################
  if (jsv_sub_is_param('l_hard','h_vmem')){
    my $h_vmem = jsv_sub_get_param('l_hard','h_vmem');
    # large memory requests go to himem node in whole.q
    # regardless of how many slots were requested
    # remove any memory limits - job has the whole node
    if ($h_vmem =~ s/g$//i){
      if ($h_vmem >= $mem_threshold){
        jsv_sub_del_param('l_hard', 'h_vmem');
        jsv_set_param('q_hard', 'whole.q');
        jsv_sub_add_param('l_hard', 'himem=true');
        # we're done, correct and submit
        if ($debug) {
          jsv_log_info("--- CORRECTED PARAMS ---");
          jsv_show_params();
          jsv_reject();
        } else {
          jsv_correct();
        }
      }
    }
  }

  ############################################################################################
  # Parallel Jobs
  #   > 12 slots go to whole.q (where exclusive=true), disregard memory limits
  #   < 12 slots go to slice.q (i.e. shared nodes)
  #############################################################################################
  if (jsv_get_param('pe_name')){
    if ($params{pe_min} >= $slot_threshold){
      jsv_set_param('q_hard', 'whole.q');
      jsv_sub_del_param('l_hard', 'h_vmem') if jsv_sub_is_param('l_hard', 'h_vmem');
    } else {
      jsv_set_param('q_hard', 'slice.q');
      # set a default memory limit if user has not specified one
      if (! jsv_sub_get_param('l_hard', 'h_vmem')){
        my $memlimit;
        if (jsv_is_param('pe_max')){
          $memlimit = $params{pe_max} * $mem_multiplier;
        } else {
          $memlimit = $params{pe_min} * $mem_multiplier;
        }
        jsv_sub_add_param('l_hard', "h_vmem=$memlimit" . "g");
      }
    }
  } else {
    jsv_set_param('q_hard', 'slice.q');
    if (! jsv_sub_get_param('l_hard', 'h_vmem')){
      jsv_sub_add_param('l_hard', "h_vmem=$mem_multiplier" . "g");
    }
  }

  if ($debug) {
    jsv_log_info("--- CORRECTED PARAMS ---");
    jsv_show_params();
    jsv_reject();
  } else {
    jsv_correct();
  }
  return;
}); 

jsv_main();
