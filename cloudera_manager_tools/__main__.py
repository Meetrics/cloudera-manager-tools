#!/usr/bin/env python
# TODO: modularize
from argparse import ArgumentParser, RawTextHelpFormatter
from cm_api.api_client import ApiResource

import cloudera_manager_tools as cmt

# TODO: get password from STDIN
# TODO: add config file options
# TODO: add sub-commands
def _create_argparser():
    parser = ArgumentParser(description="Cloudera Manager Tools", formatter_class=RawTextHelpFormatter)
    
    cm_conn_group = parser.add_argument_group('Cloudera Manager Connection')
    cm_conn_group.add_argument( '-H', '--host', dest='cm_host', required=True, help='Cloudera Manager server host', metavar='HOST')
    cm_conn_group.add_argument( '-p', '--port', dest='cm_port', default='7180', help='Cloudera Manager server port (default: %(default)s)', metavar='PORT')
    cm_conn_group.add_argument( '-U', '--username', dest='cm_usr', default='admin', help='Cloudera Manager username (default: %(default)s)', metavar='USERNAME')
    cm_conn_group.add_argument( '-P', '--password', dest='cm_pwd', default='admin', help='Cloudera Manager password (default: %(default)s)', metavar='PASSWORD')
    
    parser.add_argument( 'service', metavar='SERVICE', help='Cloudera Manager Service: ' + str(_list_services()))
    parser.add_argument( 'action', metavar='ACTION', help='Action to perform for the service')
    
    return parser

def _find_svc_class(service):
    try:
        svc_module = getattr(cmt, service)
        svc_class = getattr(svc_module, service.title())
    except:
        raise Exception( 'service "'+service+'" not recognized.' )
    
    return svc_class

def _exec_svc_action(cm_client, service, action):
    svc_class = _find_svc_class(service)
    try:
        svc_obj = svc_class(cm_client)
        svc_action_method = getattr( svc_obj, action.replace('-','_') )
    except:
        raise Exception( 'action "'+action+'" not recognized.' )
    
    return svc_action_method()

def _list_services():
    return filter( lambda meth: not meth.startswith('_'), dir(cmt) )

def _list_actions(service):
    svc_class = _find_svc_class(service)
    return filter( lambda meth: not meth.startswith('_'), dir(svc_class) )

def main():
    parser = _create_argparser()
    args = parser.parse_args()
    cm_client = ApiResource(args.cm_host, username=args.cm_usr, password=args.cm_pwd, server_port=args.cm_port)
    try:
        res = _exec_svc_action(cm_client, args.service, args.action)
        if(res): print res
    except Exception as e:
        parser.error( str(e) )

if __name__ == '__main__':
  main()
