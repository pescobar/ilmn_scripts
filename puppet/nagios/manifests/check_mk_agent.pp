# adapted from http://weblog.etherized.com/posts/186
class nagios::check_mk_agent {
  # Definitions
  # If nagios_server is defined as a node classifier use that, otherwise use the value specified here
  if $nagios_server {
  } else {
    $nagios_server = "10.1.1.3"
  }

  # Where the configs ultimately go; if you run a recent check_mk you can use a subdirectory of conf.d if you wish
  # as above this may be set in the classifier, but be sure all nodes running the agent have this in their scope
  if $mk_confdir {
  } else {
    $mk_confdir = "/etc/check_mk/conf.d"
  }

  # we need the agent package...
  package { "check_mk-agent": 
    ensure => installed,
  }

  # this template restricts check_mk access to the nagios_server specified above
  file { "/etc/xinetd.d/check_mk":
    ensure  => file,
    content => template("nagios/check_mk.erb"),
    mode    => 644,
    owner   => root,
    group   => root,
  }

  # the exported file resource
  # the template will create a valid check_mk configuration file on the nagios server for each monitored host
  # the notify will then perform the initial check_mk inventory on that host
  @@file { "$mk_confdir/$fqdn.mk":
    content => template("nagios/collection.mk.erb"),
    notify  => Exec["checkmk_inventory_$fqdn"],
    tag     => "checkmk_conf",
  }

  # the exported exec resource
  # this will trigger a check_mk inventory of the specific node whenever its config changes
  @@exec { "checkmk_inventory_$fqdn":
    command     => "/usr/bin/check_mk -I $fqdn",
    notify      => Exec["checkmk_refresh"],
    refreshonly => true,
    tag         => "checkmk_inventory",
  }
}
