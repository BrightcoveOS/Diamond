import facet

FACET_MODULE_LOADAVG = 'loadavg'
FACET_MODULE_CPU = 'cpu'
FACET_MODULE_MEMORY = 'memory'
FACET_MODULE_NETWORK = 'network'
FACET_MODULE_DISK = 'disk'

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
        
        Arguments:
        cpu -- return count for the given cpu, or total cpu if none
        """
        raise NotImplementedError() 

    def get_cpu_counters_max(self, counter):
        """
        Return the max value for a cpu usage counter
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

    def get_interfaces(self):
        """
        Return a list of interfaces present on the system 
        """
        raise NotImplementedError() 

    def get_interface_counters(self, interface):
        """
        Return a dict of network stat counters for the specified interface 
        """
        raise NotImplementedError()
    
    def get_interface_counters_max(self, counter):
        """
        Return the max value for a network stat counter
        """
        raise NotImplementedError()

class DiskStatModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_DISK

    def get_mounts(self):
        """
        Return a list of mounted filesystems
        """
        raise NotImplementedError() 

    def get_disks(self):
        """
        Return a list of disks
        """
        raise NotImplementedError()
        
    def get_disk_counters(self, disk):
        """
        Return a dict of disk stat counters for the specified disk
        """
        raise NotImplementedError()
    
    def get_disk_counters_max(self, counter):
        """
        Return the max value for a disk usage counter
        """
        raise NotImplementedError()

    def get_disk_space_total(self, disk):
        raise NotImplementedError() 

    def get_disk_space_used(self, disk):
        raise NotImplementedError() 

    def get_disk_space_free(self, disk):
        raise NotImplementedError() 
