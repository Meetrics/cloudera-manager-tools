#!/usr/bin/env python

# Get a handle to the API client
from cm_api.api_client import ApiResource
from datetime import datetime, timedelta
from os import path
import sys, time

try:
    cm_host = sys.argv[1]
    cm_port = int(sys.argv[2])
    cm_usr = sys.argv[3]
    cm_pwd = sys.argv[4]
except:
    print("""Usage: %s HOST PORT USERNAME PASSWORD
List Cloudera hosts by role.
""" % path.basename(sys.argv[0]))
    exit(1)

api = ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port)

# Get a list of all clusters
cluster = None
for c in api.get_all_clusters():
  #print c.name
  if c.name == "cluster":
    cluster = c

if cluster:
  yarn = None
  for s in cluster.get_all_services():
    #print s
    if s.type == "YARN":
      yarn = s

  if yarn:
    rm = []
    for r in yarn.get_all_roles():
      #print r.type
      if r.type == 'RESOURCEMANAGER':
        rm.append(r)
    #active_rm = None
    #for n in rm:
    #  #print n
    #  active_rm = n.name

    to_time = datetime.now()
    from_time = to_time - timedelta(hours=1)
    running = []
    ts = api.query_timeseries('select total_containers_running_across_nodemanagers where serviceName="yarn"', from_time, to_time)
    #print ts
    for response in ts:
      if response.warnings:
        print >> sys.stderr, "Warnings: %s" % (response.warnings)
      if response.errors:
        print >> sys.stderr, "Errors: %s" % (response.errors)
      if response.timeSeries:
        for timeseries in response.timeSeries:
          metadata = timeseries.metadata
          if timeseries.data:
            #print timeseries.data
            previous = 9000
            for d in timeseries.data:
              if d.value <= previous:
                running.append(d.value)
                previous = d.value
              else:
                running = []
    pending = []
    ts = api.query_timeseries('select pending_containers_cumulative where category=YARN_POOL and serviceName="yarn" and queueName=root', from_time, to_time)
    #print ts
    for response in ts:
      if response.warnings:
        print >> sys.stderr, "Warnings: %s" % (response.warnings)
      if response.errors:
        print >> sys.stderr, "Errors: %s" % (response.errors)
      if response.timeSeries:
        for timeseries in response.timeSeries:
          metadata = timeseries.metadata
          if timeseries.data:
            #print timeseries.data
            for d in timeseries.data:
              if d.value > 500:
                pending.append(d.value)
              else:
                pending = []
    #print ts
    for n in rm:
      gctime = []
      ts = api.query_timeseries('select integral(jvm_gc_time_ms_rate) where entityName="'+n.name+'"', from_time, to_time)
      for response in ts:
        if response.warnings:
          print >> sys.stderr, "Warnings: %s" % (response.warnings)
        if response.errors:
          print >> sys.stderr, "Errors: %s" % (response.errors)
        if response.timeSeries:
          for timeseries in response.timeSeries:
            metadata = timeseries.metadata
            if timeseries.data:
              #print timeseries.data
              for d in timeseries.data:
                if d.value > 100:
                  gctime.append(d.value)
                else:
                  gctime = []
      #print len(running), len(pending), len(gctime)
      if len(running) > 30 and len(pending) > 30 and len(gctime) > 30:
        print "restarting "+n.name
        cmdlist = yarn.restart_roles(n.name)
        for cmd in cmdlist:
          cmd.wait()
        print "now sleeping for one hour"
        time.sleep(3600)
        break
    """
    for n in rm:
      #print n
      metrics = n.get_metrics()
      for m in metrics:
        print "%s (%s)" % (m.name, m.unit)
      cmdlist = hdfs.restart_roles(n)
      for cmd in cmdlist:
        cmd.wait()
    """
## -- Output --
# Cluster 1 - CDH4
# Cluster 2 - CDH3

