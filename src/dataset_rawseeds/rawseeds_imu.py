import numpy as np
from rawlogs.library import RawTextLog


__all__ = ['RawseedsIMU']


class RawseedsIMU(RawTextLog):
    ''' 
    Read an IMU log file in Rawseeds format.
    
    File format: ::
            
        IMU:
        Timestamp [seconds.microseconds]
        Sample counter (modulo 2^16 -1) [unitless]
        Acceleration along X [m/s^2]
        Acceleration along Y [m/s^2]
        Acceleration along Z [m/s^2]
        Angular velocity around X [rad/s]
        Angular velocity around Y [rad/s]
        Angular velocity around Z [rad/s]
        Earth's megnetic field along X [?]
        Earth's megnetic field along Y [?]
        Earth's megnetic field along Z [?]
        R1..R9 Orientation matrix, row after row [unitless]

    Example: ::
    
        1235562390.080244, 34262,   0.029,  -0.152,   9.786,  -0.001,   \
            0.002,  -0.014,   0.296,  -0.462,  -0.718,   0.1325,  -0.9912,   \
            0.0005,   0.9910,   0.1325,  -0.0169,   0.0167,   0.0027,   0.9999
        
'''

    def __init__(self, filename):
        dtypes = {}
        dtypes['counter'] = np.dtype(('int64', 1))
        dtypes['acceleration'] = np.dtype(('float', 3))
        dtypes['angular_velocity'] = np.dtype(('float', 3))
        dtypes['magnetic_field'] = np.dtype(('float', 3))
        dtypes['attitude'] = np.dtype(('float', (3, 3)))

        parse_function = rawseeds_imu_parse

        RawTextLog.__init__(self,
                            filename=filename,
                            dtypes=dtypes,
                            parse_function=parse_function)



def rawseeds_imu_parse(line):
    """ returns a tuple (timestamp, array of (name, value) )"""
    elements = map(str.strip, line.split(","))
    if len(elements) != 20:
        msg = ('Invalid format; expected 20, got %d elements: %r' %
               (len(elements), line))
        raise ValueError(msg)

    timestamp = float(elements.pop(0))
    counter = int(elements.pop(0))

    def read_vector(n=3):
        a = np.zeros(n)
        for i in range(n):
            a[i] = float(elements.pop(0))
        return a

    acceleration = read_vector(3)
    angular_velocity = read_vector(3)
    magnetic_field = read_vector(3)
    attitude = read_vector(9).reshape((3, 3))

    return [
        (timestamp, 'counter', np.array(counter, dtype='int64')),
        (timestamp, 'acceleration', np.array(acceleration)),
        (timestamp, 'angular_velocity', np.array(angular_velocity)),
        (timestamp, 'magnetic_field', np.array(magnetic_field)),
        (timestamp, 'attitude', np.array(attitude)),
    ]

