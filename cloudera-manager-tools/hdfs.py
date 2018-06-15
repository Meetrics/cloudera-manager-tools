#!/usr/bin/env python

import sys
from os import path
from cm_api.api_client import ApiResource

class CmHdfs:
  
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
  
  def __hdfs_datanodes(self):
    hdfs = self.__hdfs_service()
    
    datanodes = []
    if hdfs:
      for role in hdfs.get_all_roles():
        if role.type == 'DATANODE':
          datanodes.append(role)
    
    return datanodes
  
  def health(self):
    return self.__hdfs_service().healthChecks
    
  def datanodes_health(self):
    dns_health = []
    for dnode in self.__hdfs_datanodes():
      dns_health.append({ dnode.name: dnode.healthChecks })
    
    return dns_health
  
  def rolling_restart(self):
    hdfs = self.__hdfs_service()
    cmdlist = hdfs.restart_roles( map(lambda dn: dn.name, self.__hdfs_datanodes()) )
    for cmd in cmdlist:
      cmd.wait()

if __name__ == '__main__':
 # TODO: dirty, modularize
 try:
   cm_host = sys.argv[1]
   cm_port = int(sys.argv[2])
   cm_usr = sys.argv[3]
   cm_pwd = sys.argv[4]
   hdfs_action = sys.argv[5]
 except:
    print("""Usage: %s HOST PORT USERNAME PASSWORD ACTION
Perform action on the HDFS service.

ACTION: can be one of health, datanodes-health, rolling-restart
""" % path.basename(sys.argv[0]))
    exit(1)
  
 cmHdfs = CmHdfs( ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port) )
 res = getattr(cmHdfs, hdfs_action.replace('-','_'))()
 if(res): print res
