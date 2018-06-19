#!/usr/bin/env python

from cloudera_manager_tools.__interfaces__ import AbsCmtServiceModule

class Spark( AbsCmtServiceModule ):
  
  _svc_type = 'SPARK2_ON_YARN'
  
  # PUBLIC CMT ACTIONS
  
  def gateways(self):
    gateways = []
    spark = self._get_service()
    if spark:
        for role in spark.get_all_roles():
            if role.type == 'GATEWAY':
                gateways.append(role.hostRef.hostId)
    
    return map( lambda host: host.ipAddress, filter(lambda host: host.hostId in gateways, self._cm_client.get_all_hosts()) )
