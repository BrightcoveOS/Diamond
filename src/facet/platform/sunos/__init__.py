all = ['FacetSunOSProvider']

import facet

class FacetSunOSProvider(facet.FacetProvider):
    _provider_classes = ['loadavg', 'cpu', 'network'] 
    pass
