import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

import facet
import facet.modules

class SunOSDiskStatModuleTest(testsunos.AbstractSunOSTest):

    def test_get_disk_stats(self):

        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        module.get_disks()
