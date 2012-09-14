import sys

def get_platform_provider_name(platform):
    if platform in ['linux', 'linux2']:
        return 'linux'
    if platform in ['sunos', 'sunos5']:
        return 'sunos' 
    raise NotImplementedError("Platform not supported: %s" % platform)

# Import platform specific utils
platform_provider_name = get_platform_provider_name(sys.platform)

if platform_provider_name == 'sunos':
    from sunos_utils import * 
elif platform_provider_name == 'linux':
    pass
    # todo: linux native utils?
