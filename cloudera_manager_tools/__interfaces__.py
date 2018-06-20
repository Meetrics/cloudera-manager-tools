import abc

class AbsCmtModule( object ):
    __metaclass__ = abc.ABCMeta
    
    _cm_client = None
    _cluster = None
    
    def __init__(self, cm_client, cluster):
        self._cm_client = cm_client
        self._cluster = cluster
    
    @abc.abstractproperty
    def _cmt_description(self):
        pass
    
    def _get_cluster(self):
        return self._cm_client.get_cluster(self._cluster)
    
class AbsCmtServiceModule( AbsCmtModule ):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractproperty
    def _cmt_svc_type(self):
        pass
    
    # TODO: for now we assume we have one service at max for each service type
    def _get_service(self):
	svcs = [svc for svc in self._get_cluster().get_all_services() if svc.type == self._cmt_svc_type]
	return svcs[0] if len(svcs) else None
