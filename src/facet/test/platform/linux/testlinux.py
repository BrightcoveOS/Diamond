import unittest

import testfacet

import facet.platform.linux

class AbstractLinuxTest(testfacet.AbstractFacetModuleTest):
    
    def get_platform_provider(self):
        return facet.platform.linux.LinuxProvider 
    
