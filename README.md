At some point, you may need to run:

	sudo apt-get update


Clone me:

	git clone https://github.com/jasonjmcghee/vagrantWorkspace.git

	cd vagrantWorkspace/


Install vagrant:

	sudo dpkg --install vagrant\_1.2.3\_x86\_64.deb


Install setuptools:

	sudo python ez\_setup.py


Install python-vagrant:

	cd python-vagrant

	sudo python setup.py install


Install pip, fabric, python-crypto:

	sudo apt-get install python-pip

	sudo apt-get install python-crypto

	sudo pip install fabric


Add the vagrant boxes we need:

	vagrant box add raring64 http://dl.dropbox.com/u/13510779/lxc-raring-amd64-2013-05-08.box &

	vagrant box add raring64 http://cloud-images.ubuntu.com/vagrant/raring/current/raring-server-cloudimg-amd64-vagrant-disk1.box


Install virtualbox (yeah... it's big. sorry.):

	sudo apt-get install virtualbox

Kernal related errors can _usually be fixed with:

	sudo apt-get install build-essential linux-headers-`uname -r`
	sudo dpkg-reconfigure virtualbox-dkms 
	sudo dpkg-reconfigure virtualbox

Create inception!
	
	python startVm.py
