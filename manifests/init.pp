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

class vagrant {
	package { 'vagrant':
		provider => dpkg,
		ensure => installed,
		source => "/vagrant/vagrant_1.2.3_x86_64.deb"
	}

	package { "fabric":
    		ensure => "1.6.1",
    		provider => pip,
	}

	exec { 'python-vagrant':
		cwd	=> "/vagrant/python-vagrant/",
		command => "/usr/bin/python setup.py install",
		require => Exec['install-vagrant-lxc'],
        }

	file { 'test.py':
		path => '/home/vagrant/test.py',
		ensure => file,
		source => "/vagrant/test.py",
	}
	
	file { 'clean.py':
		path => '/home/vagrant/clean.py',
		ensure => file,
		source => "/vagrant/clean.py"
	}

	exec { 'install-vagrant-lxc':
		command => '/usr/bin/vagrant plugin install vagrant-lxc', 
		require => Exec['fix-vagrant-home'],
	}

	exec { 'fix-vagrant-home':
		command => "/bin/echo 'export VAGRANT_HOME=/home/vagrant/.host.vagrant.d' >> /home/vagrant/.profile",
		require => Package['vagrant'],
	}

	exec { 'setup-env':
		command => '/usr/bin/python test.py lxc',
		cwd	=> "/home/vagrant/",
		require => Exec['python-vagrant'],
	}
}

include init
include python
include vagrant
