class test {

	file { '/home/vagrant/readme.txt':
		ensure => present,
		content => "Hello, World! -Robot Aaron",
	}
}	

include test
