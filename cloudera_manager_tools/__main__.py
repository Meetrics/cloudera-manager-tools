#!/usr/bin/env python
import sys
from os import path
from cm_api.api_client import ApiResource

import cloudera_manager_tools as cmt

# TODO: dirty, improve
def main():
    try:
        cm_host = sys.argv[1]
        cm_port = int(sys.argv[2])
        cm_usr = sys.argv[3]
        cm_pwd = sys.argv[4]
        service = sys.argv[5]
        action = sys.argv[6]
    except:
        print("""Usage: %s HOST PORT USERNAME PASSWORD SERVICE ACTION
Perform action on the specified service.
""" % path.basename(sys.argv[0]))
        exit(1)
    
    module = __import__("cloudera_manager_tools."+service)
    mService = getattr(module, service)
    
    cm_client = ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port)
    service_obj = getattr(mService, service.title())( cm_client )
    
    getattr( service_obj, action.replace('-','_') )()
    if(res): print res

if __name__ == '__main__':
  main()
