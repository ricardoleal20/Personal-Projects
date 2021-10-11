"""
@author: Andrew Abi-Mansour 
"""

import numpy as np
import pandas as pd

def writeOutput(filename, natoms, timestep, box, **data):
    """ Writes the output (in dump format) """

    box = [(-box/2, box/2), (-box/2,box/2), (-box/2,box/2)]
    
    axis = ('x', 'y', 'z')
    
    with open(filename, 'a') as fp:
        
        fp.write('ITEM: TIMESTEP\n')
        fp.write('{}\n'.format(timestep))
        
        fp.write('ITEM: NUMBER OF ATOMS\n')
        fp.write('{}\n'.format(natoms))
        
        fp.write('ITEM: BOX BOUNDS' + ' f' * len(box) + '\n')
        for box_bounds in box:
            fp.write('{} {}\n'.format(*box_bounds))

        for i in range(len(axis) - len(box)):
            fp.write('0 0\n')
            
        keys = list(data.keys())
        
        for key in keys:
            isMatrix = len(data[key].shape) > 1
            
            if isMatrix:
                _, nCols = data[key].shape
                
                for i in range(nCols):
                    if key == 'pos':
                        data['{}'.format(axis[i])] = data[key][:,i]
                    else:
                        data['{}_{}'.format(key,axis[i])] = data[key][:,i]
                        
                del data[key]
                
        keys = data.keys()
        
        fp.write('ITEM: ATOMS' + (' {}' * len(data)).format(*data) + '\n')
        
        output = []
        for key in keys:
            output = np.hstack((output, data[key]))
            
        if len(output):
            np.savetxt(fp, output.reshape((natoms, len(data)), order='F'))

def writeOutput_python(file,natoms,timestep, box, position, v):

    for pos in position:
        file.write(str(timestep)); file.write(' ')
        file.write(str(pos[0])); file.write(' '); file.write(str(pos[1])); file.write(' '); file.write(str(pos[2]))
        file.write('\n')