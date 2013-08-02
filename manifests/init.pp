stage { "pre": before => Stage["main"] }
class python {
    exec { 'apt-get update':
  	command => '/usr/bin/sudo /usr/bin/apt-get update'
    }
    package {
        "build-essential": ensure => latest;
        "python": ensure => "2.7.4-0ubuntu1";
        "python-dev": ensure => "2.7.4-0ubuntu1";
        "python-setuptools": ensure => installed;
    }
    exec { "easy_install pip":
        path => "/usr/local/bin:/usr/bin:/bin",
        refreshonly => true,
        require => Package["python-setuptools"],
        subscribe => Package["python-setuptools"],
    }
}
class { "python": stage => "pre" }

class init {
	package { 'lxc': 
		ensure => "installed",
		require => Exec['apt-get update'],
	}

	package { 'git':
		ensure => "installed",
		require => Exec['apt-get update'],
	 }
}


class { "init": stage => "main" }

class vagrant {
	package { 'vagrant':
		provider => dpkg,
		ensure => installed,
		source => "/vagrant/vagrant_1.2.3_x86_64.deb",
		require => File['start-inside.py']
	}

	package { "fabric":
    		ensure => "1.6.1",
    		provider => pip,
	}

	file { 'copy-python-vagrant':
		path => '/home/vagrant/python-vagrant',
		ensure => directory,
		recurse => true,
		source => "/vagrant/python-vagrant",
		require => Exec['install-vagrant-lxc'],
	}

	exec { 'python-vagrant':
		cwd	=> "home/vagrant/python-vagrant/",
		path => ["/usr/bin/","/usr/sbin/","/bin"],
		command => "sudo python setup.py install",
		require => File['copy-python-vagrant'],
        }

	file { 'start-inside.py':
		path => '/home/vagrant/start-inside.py',
		ensure => file,
		source => "/vagrant/vm-inside/start-inside.py",
	}

	file { 'manifests':
		path => '/home/vagrant/manifests',
		ensure => directory,
		recurse => true,
		source => "/vagrant/vm-inside/manifests",
	}

	
	exec { 'install-vagrant-lxc':
		command => '/usr/bin/vagrant plugin install vagrant-lxc', 
		require => Exec['fix-vagrant-home'],
	}

	exec { 'fix-vagrant-home':
		command => "/bin/echo 'export VAGRANT_HOME=/home/vagrant/.host.vagrant.d' >> /home/vagrant/.profile",
		require => Package['vagrant'],
	}

}
class { "vagrant": stage => "main" }

stage { "post":  }
class finish {

	file { '/home/vagrant/.vagrant/':
		mode => 0777,
		recurse => true,
		ensure => directory,
		require => Exec['python-vagrant'],
	}

	exec { 'final':
		path => ["/usr/bin/","/usr/sbin/","/bin"],
		command => 'python start-inside.py',
		cwd	=> "/home/vagrant/",
	}

	exec { 'final2':
		path => ["/usr/bin/","/usr/sbin/","/bin"],
		command => 'python start-inside.py',
		cwd	=> "/home/vagrant/",
		require => File['/home/vagrant/.vagrant/'],
	}
}
class { "finish": stage => "post" }
Stage["main"] -> Stage['post']


include init
include python
include vagrant
include finish
