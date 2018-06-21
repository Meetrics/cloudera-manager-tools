#!/usr/bin/env python

# TODO: modularize
from argparse import ArgumentParser, RawTextHelpFormatter
from cm_api.api_client import ApiResource

from cloudera_manager_tools.__version__ import VERSION
import cloudera_manager_tools.__helpers__ as cmt_helpers

# TODO: PEP8 code documentation
# TODO: get password from STDIN
# TODO: add config file options to specify API server connection
# TODO: ??? add argcomplete ???
def _create_argparser():
    parser = ArgumentParser(description='Cloudera Manager Tools: easily perform common tasks using the CM API.', formatter_class=RawTextHelpFormatter)
    
    cm_conn_group = parser.add_argument_group('Cloudera Manager API server connection')
    cm_conn_group.add_argument( '-H', '--host', dest='cm_host', required=True, help='Cloudera Manager server host', metavar='HOST')
    cm_conn_group.add_argument( '-p', '--port', dest='cm_port', default='7180', help='Cloudera Manager server port (default: %(default)s)', metavar='PORT')
    cm_conn_group.add_argument( '-U', '--username', dest='cm_usr', default='admin', help='Cloudera Manager username (default: %(default)s)', metavar='USERNAME')
    cm_conn_group.add_argument( '-P', '--password', dest='cm_pwd', default='admin', help='Cloudera Manager password (default: %(default)s)', metavar='PASSWORD')
    
    parser.add_argument( '-v', '--version', action='version', version='Cloudera Manager Tools ' + VERSION)
    # TODO: add possibility to query multiple clusters?
    parser.add_argument( '-C', '--cluster', dest='cluster', default='cluster', help='Cluster name (default: %(default)s)', metavar='CLUSTERNAME')
    
    # Add a subcommand for each defined CMT (service) module
    subparsers = parser.add_subparsers(dest="cmt_service", metavar='SERVICE', help='Clouder Manager Tools Service')
    for cmt_svc in cmt_helpers.list_cmt_services():
        subparser = subparsers.add_parser(cmt_svc, help=cmt_helpers.find_svc_class(cmt_svc)._cmt_description )
	subparser.add_argument( 'cmt_action', choices=cmt_helpers.list_cmt_actions(cmt_svc), metavar='ACTION', help='Action to perform on ' + cmt_svc + ': %(choices)s')
    
    return parser

def main():
    parser = _create_argparser()
    args = parser.parse_args()
    cm_client = ApiResource(args.cm_host, username=args.cm_usr, password=args.cm_pwd, server_port=args.cm_port)
    try:
        res = cmt_helpers.exec_svc_action(cm_client, args.cluster, args.cmt_service, args.cmt_action)
	cmt_helpers.hprint(res)
    except Exception as e:
	parser.error( str(e) )

if __name__ == '__main__':
  main()
