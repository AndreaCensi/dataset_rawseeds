import numpy as np
from rawlogs.library import RawTextLog


__all__ = ['RawseedsRF']


class RawseedsRF(RawTextLog):
    ''' This block reads a range-finder log in Rawseeds format. 
    
    File format: ::
        
        Timestamp [seconds.microseconds]
        # of ranges [unitless]
        Angular offset [1/4 degree]
        R1..R181 Ranges (zero padded to 181 ranges) [m]
    
    '''
    def __init__(self, filename, signal_name):
        dtypes = {}
        dtypes[signal_name] = np.dtype(('float', 181))
        parse_function = RFParse(signal_name)
        RawTextLog.__init__(self,
                            filename=filename,
                            dtypes=dtypes,
                            parse_function=parse_function)
        

class RFParse():
    def __init__(self, signal_name):
        self.signal_name = signal_name

    def __call__(self, line):
        """ returns a tuple (timestamp, array of (name, value) )"""
        elements = line.split(',')
        timestamp = float(elements[0])
        #num_readings = int(elements[1]) 
        #offset = float(elements[2]) 
        readings = np.array(map(float, elements[3:]))
        return [(timestamp, self.signal_name, readings)]

 
