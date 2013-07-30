exec { 'clone-vm-inside':
	cwd     => "/home/vagrant/",
	command => '/usr/bin/git clone https://github.com/IDSGPlayground/vm-inside.git',
	require => Exec['python-vagrant'],
}
