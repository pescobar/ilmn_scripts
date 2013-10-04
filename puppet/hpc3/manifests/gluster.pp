class gluster {
  # define a pair of peer gluster servers
  # NOTE: gluster module satisfies package and service requirements
  class { 'glusterfs::server':
    peers => $::hostname ? {
      'c0-0' => '10.1.3.11',
      'c0-1' => '10.1.3.10',
    }
  } -> 

  # create a volume on the peers
  glusterfs::volume { 'gv0':
    create_options => 'replica 2 10.1.3.10:/data 10.1.3.11:/data',
  }

  # add to fstab - but don't mount (yet)
  glusterfs::mount { '/mnt/gluster':
    ensure => 'present',
    device => $::hostname ? {
      'c0-0' => '10.1.3.10:/gv0',
      'c0-1' => '10.1.3.11:/gv0',
    }
  }
}
