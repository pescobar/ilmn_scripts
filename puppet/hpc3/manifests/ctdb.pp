class ctdb {
  package { 'ctdb':
    ensure => installed,
  }
  service { 'ctdb':
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
    require    => Mount['/mnt/gluster'],
  }
  file { '/etc/sysconfig/ctdb':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => "puppet:///modules/hpc3/ctdb",
    require => Package['ctdb'],
    notify  => Service['ctdb'],
  }
  file { '/etc/ctdb/nodes':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => "puppet:///modules/hpc3/nodes",
    require => Package['ctdb'],
    notify  => Service['ctdb'],
  }
  file { '/etc/ctdb/public_addresses':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => "puppet:///modules/hpc3/public_addresses",
    require => Package['ctdb'],
    notify  => Service['ctdb'],
  }
}
