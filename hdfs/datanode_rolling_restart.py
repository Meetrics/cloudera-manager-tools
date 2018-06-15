#!/usr/bin/env python

import sys
from os import path
# Get a handle to the API client
from cm_api.api_client import ApiResource

try:
    cm_host = sys.argv[1]
    cm_port = int(sys.argv[2])
    cm_usr = sys.argv[3]
    cm_pwd = sys.argv[4]
except:
    print("""Usage: %s HOST PORT USERNAME PASSWORD
Perform a rolling restart on datanodes.
""" % path.basename(sys.argv[0]))
    exit(1)

api = ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port)
# Get a list of all clusters
cluster = None
for c in api.get_all_clusters():
  print c.name
  if c.name == "cluster":
    cluster = c

if cluster:
  hdfs = None
  for s in cluster.get_all_services():
    print s
    if s.type == "HDFS":
      hdfs = s

  if hdfs:
    dn = []
    for r in hdfs.get_all_roles():
      if r.type == 'DATANODE':
        dn.append(r.name)

    for n in dn:
      print n
      cmdlist = hdfs.restart_roles(n)
      for cmd in cmdlist:
        cmd.wait()
## -- Output --
# Cluster 1 - CDH4
# Cluster 2 - CDH3
