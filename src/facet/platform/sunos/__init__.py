all = ['FacetSunOSProvider']

import facet
import facet.modules

class SunOSProvider(facet.FacetProvider):

    def __init__(self):
        facet.FacetProvider.__init__(self)

        self._load_provider_modules()
        
    class LoadAverageModule(facet.modules.LoadAverageModule):
        pass 

