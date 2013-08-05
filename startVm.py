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

def start(provider=None, box_name="raring64"):
	"""Starts the specified machine using vagrant"""
	info("Creating new Vagrant cell...")
	v = vagrant.Vagrant()
	info("Initializing Vagrant cell...")
	do("cp vagrant.conf Vagrantfile")
	info("Customizing Vagrantfile...")
	replaceIf("raring64", box_name, box_name != "raring64")
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

def do(command, debug=False):
   
   event = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
   if (debug):
      output = event.communicate()
      print()

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

do("vagrant ssh -c 'python start-inside.py'")
#do("vagrant status | grep 'running (' | awk '{ print $2$3 }'")
