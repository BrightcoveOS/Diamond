import os
import sys
import pprint as pp

class FacetProvider(object):
    pass

class Facet(object):
    def __init__(self):
        self._platform = sys.platform

        # Load platform provider
        self._platform_provider = self._load_platform_providers(self._platform)
 
    def _load_platform_providers(self, platform):
        # Get platform provider name
        platform_provider_name = self._get_platform_provider(platform)

        # Generate platform provider path 
        platform_provider_path = os.path.join(os.path.dirname(__file__), 'platform', platform_provider_name)

        # If the platform provider path does not exist, assume unsupported platform
        if not os.path.exists(platform_provider_path):
            raise NotImplementedError("Provider directory does not exist: %s. Platform not supported." % platform_provider_path)

        # Add platform provider path to the system path
        sys.path.append(platform_provider_path)
        
        # lets assume the platform module is called platform.<platform>
        platform_provite_module_name = '.'.join(['platform', platform_provider_name]) 

        # Import the module
        platform_provider_module =  __import__(platform_provite_module_name, globals(), locals(), ['*'])
        
    def _get_platform_provider(self, platform):
        if platform in ['linux']:
            return 'linux'
        if platform in ['sunos5']:
            return 'sunos' 
        raise NotImplementedError("Platform not supported: %s" % platform) 
     
    def __hasattr__(self, attr):
        pass

    def __getattr__(self, attr):
        if self._platform_provider:
            pass
