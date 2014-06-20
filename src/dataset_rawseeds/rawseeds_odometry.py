from rawlogs.library.textlog import RawTextLog
import numpy as np
from geometry.poses import SE2_from_xytheta

__all__ = ['RawseedsOdometry']

class RawseedsOdometry(RawTextLog):
    ''' Read an odometry log file in Rawseeds format.
    
    File format: ::
    
        Timestamp [seconds.microseconds]
        Rolling Counter [signed 16bit integer]
        TicksRight [ticks]
        TicksLeft [ticks]
        X [m]*
        Y [m]*
        Theta [rad]*

    Example: ::
    
        1235561676.443740, 3225, 0, 0, 0.000, 0.000, 0.000

    *Reference frame:* A right handed reference frame is used. 
    Y axis is aligned along the front-rear direction and points 
    towards the front, X axis is parallel to the wheelbase and points 
    towards the right wheel.

    '''

    def __init__(self, filename):
        dtypes = {}
        dtypes['pose'] = np.dtype(('float', 3))
        dtypes['pose_SE2'] = np.dtype(('float', (3,3 )))
        dtypes['ticks_right'] = np.dtype(('int64', 1))
        dtypes['ticks_left'] = np.dtype(('int64', 1))
        dtypes['x'] = np.dtype(('float', 1))
        dtypes['y'] = np.dtype(('float', 1))
        dtypes['theta'] = np.dtype(('float', 1))
        dtypes['rolling_counter'] = np.dtype(('float', 1))

        parse_function = rawseeds_odometry_parse

        RawTextLog.__init__(self,
                            filename=filename,
                            dtypes=dtypes,
                            parse_function=parse_function)



def rawseeds_odometry_parse(line):
    """ returns a tuple (timestamp, array of (name, value) )"""
    elements = map(str.strip, line.split(","))
    if len(elements) != 7:
        raise ValueError('Line does not conform to rawseeds format.')

    # elements =
    # ['1235561676.004846', '3203', '0', '0', '0.000', '0.000', '0.000']

    timestamp = float(elements.pop(0))
    rolling_counter = float(elements.pop(0))
    ticks_right = int(elements.pop(0))
    ticks_left = int(elements.pop(0))
    x = float(elements.pop(0))
    y = float(elements.pop(0))
    theta = float(elements.pop(0))

    xytheta = np.array([x, y, theta])
    return [
        # XXX compensate for reference frame?
        (timestamp, 'pose', xytheta),
        (timestamp, 'pose_SE2', SE2_from_xytheta(xytheta)),
        (timestamp, 'ticks_right', np.array(ticks_right, dtype='int')),
        (timestamp, 'ticks_left', np.array(ticks_left, dtype='int')),
        (timestamp, 'x', np.array(x)),
        (timestamp, 'y', np.array(y)),
        (timestamp, 'theta', np.array(theta)),
        (timestamp, 'rolling_counter', np.array(rolling_counter)),
    ]

