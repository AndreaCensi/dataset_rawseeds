
from .rawseeds_hokuyo import *
from .rawseeds_odometry import *
from .rawseeds_imu import *
from .rawseeds_rf import *



def jobs_comptests(context):
    from conf_tools import GlobalConfig
    GlobalConfig.global_load_dirs(['dataset_rawseeds.configs'])

    # Our tests are its tests with our configuration
    from rawlogs import unittests

    from comptests import jobs_registrar
    from rawlogs import get_rawlogs_config
    jobs_registrar(context, get_rawlogs_config())
