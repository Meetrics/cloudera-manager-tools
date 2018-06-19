import abc

class AbsCmtModule( object ):
    __metaclass__ = abc.ABCMeta
    
    _cm_client = None
    _cluster = None
    
    def _get_cluster(self):
       return self._cm_client.get_cluster(self._cluster)
    
    def __init__(self, cm_client, cluster):
        self._cm_client = cm_client
        self._cluster = cluster
    
class AbsCmtServiceModule( AbsCmtModule ):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractproperty
    def _svc_type(self):
        pass
    
    def _get_service(self):
        return self._get_cluster().get_service(self._svc_type, self._cluster)
