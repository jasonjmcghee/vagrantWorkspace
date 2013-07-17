from subprocess import Popen, PIPE, STDOUT
import subprocess


def download_install():
   url1 = "http://files.vagrantup.com/packages/95d308caaecd139b8f62e41e7add0ec3f8ae3bd1/vagrant_1.2.3_i686.deb"
   url2 = "https://github.com/fgrehm/vagrant-lxc.git"
   wget = "wget "+url1
   gitclone = "git clone "+url2+" ."
   shell_commands = [ wget, "dpkg -i vagrant_1.2.3*", "vagrant plugin install vagrant-lxc" ]
   for shell_command in shell_commands:
   	event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
   	output = event.communicate()
