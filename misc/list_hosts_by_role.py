#!/usr/bin/env python

# Get a handle to the API client
from cm_api.api_client import ApiResource
from datetime import datetime, timedelta
from collections import defaultdict
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

# Map hostIds to hostNames
hostIdToHostNameMap = {}
for host in api.get_all_hosts():
    hostIdToHostNameMap[host.hostId] = host.hostname

# Get a list of all clusters
cluster = None
for c in api.get_all_clusters():
    if c.name == "cluster":
        cluster = c

# Map:  role -> hostIds
serviceRoleToHostIdsMap = defaultdict(list)

if cluster:
    for service in cluster.get_all_services():
        for serviceRole in service.get_all_roles():
            name = service.type + "_" + serviceRole.type
            serviceRoleToHostIdsMap[name].append(serviceRole.hostRef.hostId)

rolesForHost = []
for role, hostIds in serviceRoleToHostIdsMap.items():
    hostNames = map(lambda i: str(hostIdToHostNameMap[i]), hostIds)
    for hostName in hostNames:
        rolesForHost.append(hostName + "\t" + role)

for line in sorted(rolesForHost):
    print(line)
