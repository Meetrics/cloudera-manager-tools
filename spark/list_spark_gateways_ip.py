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
  if c.name == "cluster":
    cluster = c

gateways = []

if cluster:
  spark = None
  for service in cluster.get_all_services():
    if service.type == "SPARK2_ON_YARN":
      spark = service
      if spark:
        for role in spark.get_all_roles():
          if role.type == 'GATEWAY':
            gateways.append(role.hostRef.hostId)

for host in api.get_all_hosts():
  if host.hostId in gateways:
    print host.ipAddress
