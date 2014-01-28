import numpy as np
from rawlogs.library import RawTextLog


__all__ = ['RawseedsHokuyo']


class RawseedsHokuyo(RawTextLog):
    
    def __init__(self, filename, signal_name):
        dtypes = {}
        dtypes[signal_name] = np.dtype(('float', 682))
        parse_function = HokuyoParse(signal_name)
        RawTextLog.__init__(self,
                            filename=filename,
                            dtypes=dtypes,
                            parse_function=parse_function)
        

class HokuyoParse():
    def __init__(self, signal_name):
        self.signal_name = signal_name

    def __call__(self, line):
        """ returns a tuple (timestamp, array of (name, value) )"""
        elements = map(str.strip, line.split(','))
        timestamp = float(elements.pop(0))
        readings = np.array(map(float, elements))
        
        # XXX should be 682 ???
        # if len(elements) != 681:
        #    print elements
        #    raise Exception('Expected 681 readings instead of %s' % len(elements))
        return [(timestamp, self.signal_name, readings)]
