#!/usr/bin/env python

# Get a handle to the API client
from cm_api.api_client import ApiResource
from os import path
import sys, time

class Spark:
  
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
