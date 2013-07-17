import vagrant
from subprocess import Popen, PIPE, STDOUT
import logging
from logging import warn, error, info

def clean():
   """Starts the specified machine using vagrant"""
   count=1
   shell_commands = ['vagrant halt', 'vagrant destroy', 'rm Vagrantfile']
   for shell_command in shell_commands:
      if (count == 1): info("Halting Vagrant cell...")
      elif (count == 2): info("Destroying Vagrant cell...")
      elif (count == 3): info("Removing Vagrantfile...")
      event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
      output = event.communicate()
      count += 1

l = logging.getLogger()
l.setLevel('DEBUG')
clean()
