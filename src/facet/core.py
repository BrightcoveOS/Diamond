import os
import sys
import pprint as pp
import inspect

import facet.utils

class FacetError(Exception):
    """
    Exception for Facet
    """   
 
    def __init__(self, message):
        Exception.__init__(self, message)
    
class FacetProvider(object):
    """
    The FacetProvider class represents an collection of FacetModules implemented for a specific platform.
    """
 
    def __init__(self, **kwargs):
        self._modules = {} 
        self._options = kwargs

    def _get_loadable_modules(self):
        """
        Return a list of classes to be loaded
        """
        loadable_modules = []
        for attr in dir(self):
            cls = getattr(self, attr)
            if inspect.isclass(cls) and cls != self.__class__:
                if issubclass(cls, FacetModule):
                    loadable_modules.append(cls)
        return loadable_modules

    def _load_provider_modules(self):
        loadable_modules = self._get_loadable_modules()
        for cls in loadable_modules:
            # Initialize module
            provider_module = cls(**self._options) 
            self._modules[provider_module.get_module_type()] = provider_module

    @property
    def options(self):
        return self._options

    @property
    def modules(self):
        return self._modules

class FacetModule(object):
    """
    The FacetModule class represents a group of API for gathering metrics. FacetModules are implemented for each supported FacetProvider. 
    """  
 
    def __init__(self, **kwargs):
        self._options = kwargs 

    def update(self):
        pass

    def get_module_type(self):
        return NotImplementedError()         

class Facet(object):
    """
    The Facet class represents the API entry point for accessing FacetModules.
    """

    def __init__(self, **kwargs):
        self._platform = sys.platform
        self._options = kwargs 

        # Load platform provider
        self._provider = self._load_platform_provider(self._platform)
 
    def _load_platform_provider(self, platform):
        # Get platform provider name
        platform_provider_name = facet.utils.get_platform_provider_name(platform)

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
                    return platform_provider_class(**self._options)
     
    @property
    def provider(self):
        return self._provider

    def __getattr__(self, attr):
        module_name = str(attr)
        if module_name in self:
            return self[module_name]
        else:
            raise AttributeError("Unknown module type: %s" % module_name) 

    def __hasattr__(self, attr):
        return str(attr) in self

    def list(self):
        return self.provider.modules.keys()

    def __contains__(self, k):
        return k in self.provider.modules.keys()

    def __getitem__(self, k):
        if k not in self.provider.modules.keys():
            raise NotImplementedError("%s is not supported by %s" % (k, self.__class__.__name__))
        return self.provider.modules[k]

    def __iter__(self):
        for k in self.provider.modules.values():
            yield k 
    
