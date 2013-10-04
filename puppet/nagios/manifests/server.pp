class nagios::server {
  ######################################################################
  # this module has 3 distinct sections
  #   1: install a nagios server with check_mk components and pnp4nagios
  #   2: manage the configuration files for nagios and check_mk
  #   3: automate the ongoing configuration of check_mk agents using
  #      storeconfigs and external resources
  ######################################################################

  # resource defaults
  Exec { path    => ['/sbin','/bin','/usr/sbin','/usr/bin'] }
  Service {
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
  }

  ########################################################
  # Section 1
  #   nagios and pnp4nagios installation from yum repos
  #   check_mk server components installed from tarball
  ########################################################
  $pkglist = ['nagios','nagios-plugins-all','pnp4nagios','httpd','make','gcc-c++','mod_python','xinetd']

  package { $pkglist:
    ensure => installed,
  }

  # note: the check_mk server installation modifies this file
  #       those changes have been captured in the file referenced here
  file { '/etc/nagios/nagios.cfg':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => "puppet:///modules/nagios/nagios.cfg",
    require => Package['nagios'],
    notify  => Service['nagios'],
  }
  service { 'nagios':
    require => Package['nagios'],
  }
  service { 'httpd':
    require => Package['httpd','pnp4nagios'],
  }
  service { 'xinetd':
    require => Package['xinetd'],
  }

  # automate the installation of check_mk on the server
  # using a setup file generated from a manual installation
  $check_mk = 'check_mk-1.1.12p7'

  file { '/root/check_mk.tgz':
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
    source => "puppet:///modules/nagios/${check_mk}.tar.gz",
  }
  file { '/root/.check_mk_setup.conf':
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
    source => "puppet:///modules/nagios/check_mk_setup.conf",
  }
  exec { 'prep_checkmk':
    cwd     => '/root',
    command => 'tar xzvf /root/check_mk.tgz',
    creates => "/root/$check_mk",
  }
  exec { 'install_checkmk':
    cwd => "/root/$check_mk",
    command => "/root/$check_mk/setup.sh --yes",
    creates => '/etc/check_mk',
    notify  => Service['nagios','httpd']
  }

  # ordering rules for check_mk installation
  # check_mk files have to be there before it can be installed
  File['/root/check_mk.tgz'] -> File['/root/.check_mk_setup.conf'] -> Exec['prep_checkmk'] -> Exec['install_checkmk']

  # don't enable/start the nagios service until after check_mk is installed
  Exec['install_checkmk'] -> Service['nagios']


  #####################################################################
  # Section 2: manage nagios and check_mk configuration files
  #####################################################################
  file { '/etc/nagios/objects/commands.cfg':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => "puppet:///modules/nagios/commands.cfg",
    require => Package['nagios'],
    notify  => Service['nagios'],
  }

  # note: check_mk will dynamically handle all host and service configurations
  nagios_contact { 'it-linuxadmins':
    # include all required fields - no template needed
    ensure                        => present,
    host_notifications_enabled    => '0',
    service_notifications_enabled => '0',
    host_notification_period      => '24x7',
    service_notification_period   => '24x7',
    host_notification_options     => 'd,u,r',
    service_notification_options  => 'w,u,c,r',
    host_notification_commands    => 'notify-host-by-email',
    service_notification_commands => 'notify-service-by-email',
    require                       => Package['nagios'],
    notify                        => Exec['chmod_nagios'],
    #email    => "it-linuxadmins@illumina.com",
  }
  nagios_contactgroup { 'linux-admins':
    ensure  => present,
    alias   => 'linux-admins',
    members => 'it-linuxadmins',
    require => Package['nagios'],
    notify  => Exec['chmod_nagios'],
  }

  # check_mk main configuration file
  # use this to define excluded checks, etc
  file { '/etc/check_mk/main.mk':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    before  => Exec["checkmk_inventory_$fqdn"],
    notify  => Exec["checkmk_refresh"],
    source  => "puppet:///modules/nagios/main.mk",
  }

  # note: puppet's builtin nagios resources (e.g. nagios_contact and
  #       nagios_contactgroup set perms as root:root 0600
  #       this hack resets them to what we actually need...
  exec { 'chmod_nagios':
    command     => '/bin/chmod 0644 /etc/nagios/nagios_*.cfg',
    refreshonly => true,
    notify      => Service['nagios'],
  }

  ######################################################################
  # Section 3: check_mk automation
  #   from the check_mk module by jthornhill:
  #     https://github.com/jthornhill/puppet-checkmk
  #   this is the magic that automatically adds new nodes,
  #   inventories them and refreshes nagios
  ######################################################################
  if $mk_confdir {
  } else {
    $mk_confdir = "/etc/check_mk/conf.d"
  }
  # this exec statement will cause check_mk to regenerate the nagios
  # config and restart nagios on the nagios server when new nodes are added
  exec { "checkmk_refresh":
    command => "/usr/bin/check_mk -O",
    refreshonly => true,
  }

  # collect the exported resource from the clients
  # each one will have a corresponding config file placed on the check_mk server
  # see check_mk_agent.pp for the definition of these resources
  File <<| tag == 'checkmk_conf' |>> {
  }

  # in addition, each one will have a corresponding exec resource, used to re-inventory changes
  Exec <<| tag == 'checkmk_inventory' |>> {
  }

  # finally, we prune any not-managed-by-puppet files from the directory, and refresh nagios when we do so
  # NB: for this to work, your $mk_confdir must be totally managed by puppet; if it's not you should disable
  # this resource. Newer versions of check_mk support reading from subdirectories under conf.d, so you can dedicate
  # one specifically to the generated configs
  file { "$mk_confdir":
    ensure => directory,
    purge => true,
    recurse => true,
    notify => Exec["checkmk_refresh"],
  }
}
