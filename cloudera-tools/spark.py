#!/usr/bin/env python

# Get a handle to the API client
from cm_api.api_client import ApiResource
from os import path
import sys, time

class CmSpark:
  
  _cm_client = None
  
  def __init__(self, cm_client):
    self._cm_client = cm_client
  
  def gateways(self):
    # Get a list of all clusters
    cluster = None
    for c in self._cm_client.get_all_clusters():
      if c.name == "cluster":
        cluster = c
    
    # TODO: use filter instead of for..if ... for..if ... for..if
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
    
    return map( lambda host: host.ipAddress, filter(lambda host: host.hostId in gateways, self._cm_client.get_all_hosts()) )

if __name__ == '__main__':
 # TODO: dirty, modularize
 try:
   cm_host = sys.argv[1]
   cm_port = int(sys.argv[2])
   cm_usr = sys.argv[3]
   cm_pwd = sys.argv[4]
   spark_action = sys.argv[5]
 except:
    print("""Usage: %s HOST PORT USERNAME PASSWORD ACTION
Perform miscellaneous actions on Spark.

ACTION: gateways
""" % path.basename(sys.argv[0]))
    exit(1)

 cmSpark = CmSpark( ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port) )
 res = getattr(cmSpark, spark_action.replace('-','_'))()
 if(res): print res
