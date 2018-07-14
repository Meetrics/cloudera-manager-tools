#!/usr/bin/env python

from cloudera_manager_tools.__interfaces__ import AbsCmtServiceModule

class Hdfs( AbsCmtServiceModule ):
  
  _cmt_svc_type = 'HDFS'
  _cmt_description = "Perform different operations on the HDSF service"
  
  def _get_datanodes(self):
    return self._get_service().get_roles_by_type('DATANODE')
  
  # PUBLIC CMT ACTIONS
  
  def health(self):
    return self._get_service().healthChecks
    
  def datanodes_health(self):
    dns_health = []
    for dnode in self._get_datanodes():
      dns_health.append({ dnode.name: dnode.healthChecks })
    
    return dns_health
  
  def rolling_restart(self):
    hdfs = self._get_service()
    cmdlist = hdfs.restart_roles( map(lambda dn: dn.name, self._get_datanodes()) )
    for cmd in cmdlist:
      cmd.wait()

  def datanodes_cfg_staleness_status(self):
    dns_staleness_status = []
    for dnode in self._get_datanodes():
      dns_staleness_status.append({ dnode.name: dnode.configStalenessStatus })

    return dns_staleness_status
