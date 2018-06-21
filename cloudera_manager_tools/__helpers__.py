import cloudera_manager_tools as cmt

# Helper functions to get info on CMT modules at runtime

def find_svc_class(service):
    try:
        svc_module = getattr(cmt, service)
        svc_class = getattr(svc_module, service.title())
    except Exception as e:
        raise Exception( 'service "'+service+'" not recognized.' )

    return svc_class

def exec_svc_action(cm_client, cluster, service, action):
    svc_class = find_svc_class(service)
    try:
        svc_obj = svc_class(cm_client, cluster)
        svc_action_method = getattr( svc_obj, action )
    except Exception as e:
        svc_actions = list_cmt_actions(service)
        raise Exception( 'action "'+action+'" not recognized. Must be one of: '+ str(svc_actions) )

    return svc_action_method()

def list_cmt_services():
    return filter( lambda meth: not meth.startswith('_'), dir(cmt) )

def list_cmt_actions(service):
    svc_class = find_svc_class(service)
    return filter( lambda meth: not meth.startswith('_'), dir(svc_class) )


# Helper functions to pretty print CMT modules actions output

# human redable print
def hprint(obj):
   print "\n".join(hformat(obj))

# human readable list of lines
# TODO: store indentation level as int for each line, instead of actually indent it here (the real indentation should be performed in the hprint funtion)
def hformat(obj):

    def indent(hlines):
        return [ " " * 4 + line for line in hlines ]

    hlines = []
    # Let the functional madness begin!
    if obj:
        if isinstance(obj, dict):
            hlines = [ hline for sublist in [ [k] + indent( hformat(obj[k]) ) for k in sorted(obj.keys()) ] for hline in sublist ]
        elif isinstance(obj, list):
            hlines = [ hline for sublist in [ hformat(el) for el in obj ] for hline in sublist ]
        else:
            hlines = [ str(obj) ]

    return hlines
