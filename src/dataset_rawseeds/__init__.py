
from .rawseeds_hokuyo import *
from .rawseeds_odometry import *
from .rawseeds_imu import *
from .rawseeds_rf import *




def jobs_comptests(context):
    from comptests import jobs_registrar

    # get testing configuration directory 
    from pkg_resources import resource_filename  # @UnresolvedImport
    dirname = resource_filename("dataset_rawseeds", "configs")
    
    # load into rawlogs config
    from rawlogs import get_rawlogs_config
    config = get_rawlogs_config()
    config.load(dirname)
    
    # Our tests are its tests with our configuration
    from rawlogs import unittests
    j1 = jobs_registrar(context, config)
    return j1