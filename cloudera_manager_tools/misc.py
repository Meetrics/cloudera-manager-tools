#!/usr/bin/env python

from cloudera_manager_tools.__interfaces__ import AbsCmtModule

class Misc( AbsCmtModule ):
  
  # PUBLIC CMT ACTIONS
  
  def hosts_role(self):
    # Map hostIds to hostnames
    host_ids_names_dict = {}
    for host in self._cm_client.get_all_hosts():
        host_ids_names_dict[host.hostId] = host.hostname
    
    # Get our cluster
    cluster = self._get_cluster()
    
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
