#!/usr/bin/env python

import collectd
import thread
import time

import salt.config
import salt.runner
import salt.wheel

class SaltMasterCollecter:

  def __init__(self):
    collectd.debug('SaltMasterCollector: Initialising new instance of SaltMasterCollector')
    self.salt_opts = salt.config.master_config('/etc/salt/master')
    self.runner = salt.runner.RunnerClient(self.salt_opts)
    self.minions_up = None
    self.minions_down = None

  def read(self, data=None):
    if self.minions_up is not None:
      collectd.debug('SaltMasterCollector: reading values')
      metric_up = collectd.Values();
      metric_up.plugin = 'salt-master:minions_up'
      metric_up.type = 'gauge'
      metric_up.values = [self.minions_up]
      metric_up.dispatch()
    else:
      collectd.warning("SaltMasterCollector: minions_up value not available!")

    if self.minions_down is not None:
      metric_down = collectd.Values();
      metric_down.plugin = 'salt-master:minions_down'
      metric_down.type = 'gauge'
      metric_down.values = [self.minions_down]
      metric_down.dispatch()
    else:
      collectd.warning("SaltMasterCollector: minions_down value not available!")

  def update(self):
    try:
      self.minions_up   = len(self.runner.cmd('manage.up', []))
      self.minions_down = len(self.runner.cmd('manage.down', []))
    except:
      collectd.warning("SaltMasterCollector: Got exception while updating values. Salt-Master seems not to be running! Setting values to None.")
      self.minions_up = None
      self.minions_down = None
      time.sleep(10)

def configer(ObjConfiguration):
  collectd.debug('SaltMasterCollector: Configuring')

def initer():
  global collecter
  collecter = SaltMasterCollecter()
  try:
    thread.start_new_thread(updater,())
    collectd.debug('SaltMasterCollector: updater thread started')
  except:
    collectd.warning('SaltMasterCollector: Could not start')
    raise

def updater():
  global collecter
  while True:
    collecter.update()

def reader():
  global collecter
  collecter.read()

collecter = None

collectd.register_config(configer)
collectd.register_init(initer);
collectd.register_read(reader);
