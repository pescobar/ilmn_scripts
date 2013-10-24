class rocks::extend {
  # node files
  file {
    'extendcompute':
      path   => "/export/rocks/install/site-profiles/$rocks_version/nodes/extend-compute.xml",
      owner  => 'root',
      group  => 'root',
      mode   => '0664',
      source => "puppet:///modules/rocks/extend-compute.xml";
    'extendlogin':
      path   => "/export/rocks/install/site-profiles/$rocks_version/nodes/extend-login.xml",
      owner  => 'root',
      group  => 'root',
      mode   => '0664',
      source => "puppet:///modules/rocks/extend-login.xml";
  }
  # graph files - pull in cluster-local.xml
  file {
    'cluster-local-graph':
      path   => "/export/rocks/install/site-profiles/$rocks_version/graphs/default/cluster-local-graph.xml",
      owner  => 'root',
      group  => 'root',
      mode   => '0664',
      source => "puppet:///modules/rocks/cluster-local-graph.xml";
  } 


  # rebuild the distro when the configs change
  exec { "rocks create distro":
    path        => ["/sbin/", "/bin", "/usr/sbin", "/usr/bin", "/opt/rocks/bin" ],
    cwd         => "/export/rocks/install",
    subscribe   => File["extendcompute"],
    refreshonly => true,
  }
}
