#!/usr/bin/env python

class Hdfs:
  
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
