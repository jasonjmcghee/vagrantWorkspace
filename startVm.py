from __future__ import print_function
import vagrant
from fabric.api import env, run, execute
import logging
from logging import warn, error, info
import fileinput, os, sys
from subprocess import Popen, PIPE, STDOUT
import subprocess

def replaceIf(old, new, condition=True):
	if condition: 
	   for line in fileinput.FileInput("Vagrantfile",inplace=1):
	      line = line.replace(old, new)
	      print (line, end='')

def start(provider=None):
	"""Starts the specified machine using vagrant"""
	info("Creating new Vagrant cell...")

	v = vagrant.Vagrant()
	info("Initializing Vagrant cell...")
	v.init("raring64")
	info("Modifying Vagrantfile...")
	replaceIf("# config.vm.network :pri", "config.vm.network :pri", provider == "kvm")
	replaceIf("# config.vm.synced_folder \"../data\", \"/vagrant_data\"\n", "config.vm.synced_folder \"~/.vagrant.d/\", \"/home/vagrant/.host.vagrant.d/\"")
	replaceIf("# config.vm.provision :puppet do |puppet|", "config.vm.provision :puppet do |puppet|")
	replaceIf("#   puppet.manifests_path = \"manifests\"", "   puppet.manifests_path = \"manifests\"")
	replaceIf("#   puppet.manifest_file  = \"init.pp\"", "   puppet.manifest_file = \"init.pp\"\n  end")
	info("Booting up cell...")
	v.up(provider)
	info("Finalizing new cell...")
	if provider != "kvm":
	   env.hosts = [v.user_hostname_port()]
    	   env.key_filename = v.keyfile()
    	   env.disable_known_hosts = True
	   run("echo successful")

l = logging.getLogger()
l.setLevel('DEBUG')

def finish():
   #shell_command = "vagrant status | grep 'running (' | awk '{ print $2$3 }'"
   shell_command = "vagrant ssh -c 'python start-inside.py'"
   event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
   #output = event.communicate()
   #if output[0].find("running") != -1: 
   #   prvdr = output[0][8:len(output[0])-2]
   #   info("Successfully created new " + prvdr + " cell!")
   #else: warn("Something went horribly wrong.")
   #print()

try:
   if len(sys.argv) > 3:
      warn("usage: $ python " + sys.argv[0] + " provider [box_name]")
   elif len(sys.argv) == 2:
      execute(start, sys.argv[1])
   elif len(sys.argv) == 1:
      info("Using default provider: virtualbox.")
      execute(start, "virtualbox")
   else:
      execute(start, sys.argv[1])
      box_name = sys.argv[2]
except subprocess.CalledProcessError:
   print()
   error('Some bad things are happening...')

finish()
