#!/usr/bin/env python
# TODO: modularize
from argparse import ArgumentParser, RawTextHelpFormatter
from pprint import pprint
from cm_api.api_client import ApiResource

import cloudera_manager_tools as cmt

# TODO: get password from STDIN
# TODO: add config file options
# TODO: ??? add argcomplete ???
def _create_argparser():
    parser = ArgumentParser(description="Cloudera Manager Tools: easily perform common tasks using the CM API.", formatter_class=RawTextHelpFormatter)
    
    cm_conn_group = parser.add_argument_group('Cloudera Manager API server connection')
    cm_conn_group.add_argument( '-H', '--host', dest='cm_host', required=True, help='Cloudera Manager server host', metavar='HOST')
    cm_conn_group.add_argument( '-p', '--port', dest='cm_port', default='7180', help='Cloudera Manager server port (default: %(default)s)', metavar='PORT')
    cm_conn_group.add_argument( '-U', '--username', dest='cm_usr', default='admin', help='Cloudera Manager username (default: %(default)s)', metavar='USERNAME')
    cm_conn_group.add_argument( '-P', '--password', dest='cm_pwd', default='admin', help='Cloudera Manager password (default: %(default)s)', metavar='PASSWORD')
    
    # TODO: add possibility to query multiple clusters?
    parser.add_argument( '-C', '--cluster', dest='cluster', default='cluster', help='Cluster name (default: %(default)s)', metavar='CLUSTERNAME')
    
    # Add a subcommand for each defined CMT (service) module
    subparsers = parser.add_subparsers(dest="cmt_service", metavar='SERVICE', help='Clouder Manager Tools Service')
    for cmt_svc in _list_cmt_services():
        subparser = subparsers.add_parser(cmt_svc, help=_find_svc_class(cmt_svc)._cmt_description )
	subparser.add_argument( 'cmt_action', choices=_list_cmt_actions(cmt_svc), metavar='ACTION', help='Action to perform on ' + cmt_svc + ': %(choices)s')
    
    return parser

def _find_svc_class(service):
    try:
        svc_module = getattr(cmt, service)
        svc_class = getattr(svc_module, service.title())
    except Exception as e:
        raise Exception( 'service "'+service+'" not recognized.' )
    
    return svc_class

def _exec_svc_action(cm_client, cluster, service, action):
    svc_class = _find_svc_class(service)
    try:
        svc_obj = svc_class(cm_client, cluster)
        svc_action_method = getattr( svc_obj, action )
    except Exception as e:
        svc_actions = _list_cmt_actions(service)
	raise Exception( 'action "'+action+'" not recognized. Must be one of: '+ str(svc_actions) )
    
    return svc_action_method()

def _list_cmt_services():
    return filter( lambda meth: not meth.startswith('_'), dir(cmt) )

def _list_cmt_actions(service):
    svc_class = _find_svc_class(service)
    return filter( lambda meth: not meth.startswith('_'), dir(svc_class) )

def main():
    parser = _create_argparser()
    args = parser.parse_args()
    cm_client = ApiResource(args.cm_host, username=args.cm_usr, password=args.cm_pwd, server_port=args.cm_port)
    try:
        res = _exec_svc_action(cm_client, args.cluster, args.cmt_service, args.cmt_action)
        # TODO: improve output (make it pretty ^___^)
	if(res): pprint(res)
    except Exception as e:
	parser.error( str(e) )

if __name__ == '__main__':
  main()
