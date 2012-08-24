import os
import sys
import pprint as pp
import inspect

class FacetProvider(object):
    
    def __init__(self):
        self._modules = {} 

    def _load_provider_modules(self):
        for attr in dir(self):
            cls = getattr(self, attr)
            if inspect.isclass(cls) and cls != self.__class__:
                if issubclass(cls, FacetModule):
                    provider_module = cls()
                    self._modules[provider_module.get_module_type()] = provider_module

    def __contains__(self, k):
        return k in self._modules.keys()

    def __getitem__(self, k):
        if k not in self._modules.keys():
            raise NotImplementedError("%s is not supported by %s" % (k, self.__class__.__name__))
        return self._modules[k]

    def __iter__(self):
        for k in self._modules.keys():
            yield k 

class FacetModule(object):
   
    def __init__(self):
        pass 

    def get_module_type(self):
        return NotImplementedError()         

class Facet(object):

    def __init__(self):
        self._platform = sys.platform

        # Load platform provider
        self._platform_provider = self._load_platform_provider(self._platform)
 
    def _load_platform_provider(self, platform):
        # Get platform provider name
        platform_provider_name = self._get_platform_provider_name(platform)

        # Generate platform provider path 
        platform_provider_path = os.path.join(os.path.dirname(__file__), 'platform', platform_provider_name)

        # If the platform provider path does not exist, assume unsupported platform
        if not os.path.exists(platform_provider_path):
            raise NotImplementedError("Provider directory does not exist: %s. Platform not supported." % platform_provider_path)

        # Add platform provider path to the system path
        sys.path.append(platform_provider_path)
        
        # lets assume the platform module is called platform.<platform>
        platform_provider_module_name = '.'.join(['platform', platform_provider_name]) 

        # Import the module
        platform_provider_module =  __import__(platform_provider_module_name, globals(), locals(), ['*'])

        # Instantiate provider class
        for attr in dir(platform_provider_module):
            cls = getattr(sys.modules['.'.join(['facet', platform_provider_module_name])], attr)
            if inspect.isclass(cls):            
                if issubclass(cls, FacetProvider):
                    platform_provider_class = cls 
                    return platform_provider_class()
     
    def _get_platform_provider_name(self, platform):
        if platform in ['linux']:
            return 'linux'
        if platform in ['sunos5']:
            return 'sunos' 
        raise NotImplementedError("Platform not supported: %s" % platform) 

    def __contains__(self, k):
        pass

    def __getitem(self, k):
        pass

    def __iter__(self):
        pass 
