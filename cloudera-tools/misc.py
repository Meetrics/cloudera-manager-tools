#!/usr/bin/env python

import sys
from os import path
from cm_api.api_client import ApiResource

class CmMisc:

  _cm_client = None

  def __init__(self, cm_client):
    self._cm_client = cm_client

  def __hdfs_service(self):
    # Get a list of all clusters
    cluster = None
    for cluster in self._cm_client.get_all_clusters():
      if cluster.name == "cluster": # TODO: Check if is default name
        break

    # Get HDFS service from the right cluster
    hdfs = None
    if cluster:
      for s in cluster.get_all_services():
        if s.type == "HDFS":
          hdfs = s
          break

    return hdfs
  
  def hosts_role(self):
    # Map hostIds to hostnames
    host_ids_names_dict = {}
    for host in self._cm_client.get_all_hosts():
        host_ids_names_dict[host.hostId] = host.hostname
    
    # Get a list of all clusters
    cluster = None
    for c in self._cm_client.get_all_clusters():
        if c.name == "cluster":
            cluster = c
    
    # Map: hostIds -> role
    hostids_roles = {}
    if cluster:
        for service in cluster.get_all_services():
            for service_role in service.get_all_roles():
                hostids_roles[service_role.hostRef.hostId] = service.type + "_" + service_role.type
    
    # Map: hostname -> role
    hostnames_roles = {}
    for hostid, role in hostids_roles.items():
      hostnames_roles[host_ids_names_dict[hostid]] = role
    
    return hostnames_roles

if __name__ == '__main__':
 # TODO: dirty, modularize
 try:
   cm_host = sys.argv[1]
   cm_port = int(sys.argv[2])
   cm_usr = sys.argv[3]
   cm_pwd = sys.argv[4]
   misc_action = sys.argv[5]
 except:
    print("""Usage: %s HOST PORT USERNAME PASSWORD ACTION
Perform miscellaneous actions on Cloudera.

ACTION: hosts-role
""" % path.basename(sys.argv[0]))
    exit(1)

 cmMisc = CmMisc( ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port) )
 res = getattr(cmMisc, misc_action.replace('-','_'))()
 if(res): print res
