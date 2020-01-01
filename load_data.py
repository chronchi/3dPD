import numpy as np
import os, sys
import subprocess
import base64

def call_optiperslp(file_name, dimension='1'):
    txt_file = '/tmp/' + file_name + '.txt'   
    outputpath = '/tmp'
    bashCommand = 'optiperslp -p ' + outputpath + ' -d ' + dimension +\
                  ' -n ' + file_name + ' ' + txt_file     
    process = subprocess.run(bashCommand.split())    

def upload_data(file_input):
    print("Data upload succeeded")
    # convert to base64
    a=base64.b64decode(file_input.value)
    # convert to strings array
    data = a.decode('utf-8').splitlines()
    # convert to numpy array 
    data_final = []
    for line in data:
        data_tmp = line.split(',')
        data_final.append([float(b) for b in data_tmp])
    data_final = np.array(data_final)
    return data_final    

def load_convert_calculate(file_input, dimension='1'):
    # load file
    coord_radius = np.around(upload_data(file_input), decimals=3)
    # file name to be saved in the tmp directory
    file_name = 'abcd'
    np.savetxt(os.path.join('/tmp/', file_name + '.txt'), coord_radius, fmt='%.3f')
    # call optipers to calculate persistence diagrams and optimal cycles
    call_optiperslp(file_name, dimension = dimension) 
    return coord_radius

def load_format_pd(file_name='abcd', dimension='1'):
    file_path = '/tmp/gen_' + file_name + '_' + dimension + '.txt'
    # open gen_file_d 
    f = open(file_path)
    # split into lines 
    lines = f.read().splitlines()
    # create empty list to save persistence diagram points
    persdiag = []
    # create empty list to save vertices from each point in the diagram 
    vertice_list = []
    counter_pd = 0
    for counter, line in enumerate(lines):
        # if line starts with ;, then it is a pd point
        if ';' in line:            
            # get persistence diagram point
            pd_point = [float(line.split()[i]) for i in [1,2]]
            persdiag.append(pd_point)
            # now we will save the vertices in the coord.
            tmp_list = [] #tmp list to save the vertices as a matrix 
            for sublines in lines[counter+1:]:
                # if the line starts with ;, then it is the next pd point
                if sublines[0] == ';':
                    break
                else:
                    # find vertice indices in the subline
                    idx = sublines.split(',')[1:]
                    idx = [i.split()[0] for i in idx]
                    tmp_list.extend(idx)
            # save the tmp_list to vertice_list
            vertice_list.append(tmp_list)
            counter_pd += 1
    
    return np.array(persdiag), vertice_list

def where_is(vertices, xyz_total, file_name='abcd'):
    # open i2p file
    f = open('/tmp/gen_' + file_name + '_i2p.txt')
    # split lines from f
    lines = f.read().splitlines()
    # create empty vector to save xyz coordinates
    xyz = []
    color = []
    for line in lines:
        # split line to get index from that line
        splitting = line.split()
        idx = splitting[0]
        if idx in vertices:
            xyz.append([float(i) for i in splitting[1:4]])
            color.append(2)
    xyz = np.array(xyz)
    # now we will find the indices for each point
    idx = []
    for point in xyz:
        for counter, p in enumerate(xyz_total): 
            if p[0] == point[0] and p[1] == point[1] and p[2] == point[2]:
                idx.append(counter)
                break
    return idx

