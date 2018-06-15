#!/usr/bin/env python

# Get a handle to the API client
from cm_api.api_client import ApiResource
from datetime import datetime, timedelta
from os import path
import sys, time



if __name__ == '__main__':
 # TODO: dirty, modularize
 try:
   cm_host = sys.argv[1]
   cm_port = int(sys.argv[2])
   cm_usr = sys.argv[3]
   cm_pwd = sys.argv[4]
   yarn_action = sys.argv[5]
 except:
    print("""Usage: %s HOST PORT USERNAME PASSWORD ACTION
Perform miscellaneous actions on Yarn

ACTION: 
""" % path.basename(sys.argv[0]))
    exit(1)

 cmYarn = CmYarn( ApiResource(cm_host, username=cm_usr, password=cm_pwd, server_port=cm_port) )
 res = getattr(cmYarn, yarn_action.replace('-','_'))()
 if(res): print res
