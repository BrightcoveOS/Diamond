import facet

FACET_MODULE_LOADAVG = 'loadavg'
FACET_MODULE_CPU = 'cpu'
FACET_MODULE_MEMORY = 'memory'
FACET_MODULE_NETWORK = 'network'

class LoadAverageModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_LOADAVG 
    
    def get_load_average(self):
        """
        Return a tuple of (1 min load, 5 min load, 15 min load, total processes, running processes)
        """
        raise NotImplementedError() 
    
class CPUStatModule(facet.FacetModule):

    def get_module_type(self):
        return FACET_MODULE_CPU

    def get_cpu_count(self):
        """
        Return the number of cpu's in the system
        """
        raise NotImplementedError() 

    def get_cpu_counters(self, cpu=None):
        """
        Return a dict of cpu usage counters 
        """
        raise NotImplementedError() 

class MemoryStatModule(facet.FacetModule):

    def get_module_type(self):
        return FACET_MODULE_MEMORY
    
    def get_memory_used(self):
        """
        Return the amount of memory in bytes that is in use 
        """
        raise NotImplementedError() 

    def get_memory_total(self):
        """
        Return the amount of memory in bytes is available
        """
        raise NotImplementedError() 

    def get_memory_free(self):
        """
        Return the amount of memory in bytes that is not in use
        """
        raise NotImplementedError() 

    def get_swap_used(self):
        """
        Return the amount of swap in bytes that is in use
        """
        raise NotImplementedError() 

    def get_swap_total(self):
        """
        Return the amount of swap in bytes that is available
        """
        raise NotImplementedError() 

    def get_swap_free(self):
        """
        Return the amount of swap in bytes that is not in use
        """
        raise NotImplementedError() 

class NetworkStatModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_NETWORK
