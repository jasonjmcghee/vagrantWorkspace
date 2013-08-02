#!/usr/bin/env python

import getopt
import re
import os
import sys
import logging
from   logging import debug, info, error, warn
import fileinput, os, sys
import vagrant
from fabric.api import env, run, execute
from subprocess import CalledProcessError, Popen, PIPE, STDOUT
import subprocess

import time
import math

# Retry decorator with exponential backoff
def retry(tries, delay=3, backoff=2):
  '''Retries a function or method until it returns True.

  delay sets the initial delay in seconds, and backoff sets the factor by which
  the delay should lengthen after each failure. backoff must be greater than 1,
  or else it isn't really a backoff. tries must be at least 0, and delay
  greater than 0.'''

  if backoff <= 1:
    raise ValueError("backoff must be greater than 1")

  tries = math.floor(tries)
  if tries < 0:
    raise ValueError("tries must be 0 or greater")

  if delay <= 0:
    raise ValueError("delay must be greater than 0")

  def deco_retry(f):
    def f_retry(*args, **kwargs):
      mtries, mdelay = tries, delay # make mutable

      rv = f(*args, **kwargs) # first attempt
      while mtries > 0:
        if rv is True: # Done on success
          return True

        mtries -= 1      # consume an attempt
        time.sleep(mdelay) # wait...
        mdelay *= backoff  # make future wait longer

        rv = f(*args, **kwargs) # Try again

      return False # Ran out of tries :-(

    return f_retry # true decorator -> decorated function
  return deco_retry  # @retry(arg[, ...]) -> true decorator

@retry(2, delay=5)
def wait_for_container(config):
    v = config.v
    if v.status() != 'running':
        raise Exception('Inside {0} container failed to start!'.format(v.provider))

def initialize(opts, args):
    config = Config(opts, args)
    if os.path.exists(config.Vagrantfile):
        debug("Deleting: {0}".format(config.Vagrantfile))
        os.unlink(config.Vagrantfile)
    return config

def run(config):
    v = vagrant.Vagrant()
    config.v = v
    info("Initializing Vagrant cell...")
    info("Booting up cell...")
    shell_command = "cp /vagrant/Vagrantfile-inside Vagrantfile"
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    v.up(config.provider)
    info("Finalizing new cell...")
    env.host_string = v.user_hostname()
    env.key_filename = v.keyfile()
    env.disable_known_hosts = True
    wait_for_container(config)
    info("Successfully created new {0} cell!".format(config.provider))

def cleanup(config):
    v = config.v
    # v.halt()
    # v.destroy()

class Config():
    def __init__(self, opts, args):
        self.files = args
        self.provider = 'lxc'
        self.Vagrantfile = 'Vagrantfile'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        config = initialize(opts, args)
        run(config)
        cleanup(config)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    main()
