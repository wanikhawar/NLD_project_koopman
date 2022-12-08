# generates the displacement data for each frame/time as a row in an output file. This can be read by a script from
# Scilab/Matlab and would return SVD for the system, which can be written to the odb as a modal data using another
# script.
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import itertools

# Open ODB
odb = openOdb(path='vort_shedding.odb')

# Frames
fs = odb.steps['flow'].frames

# Open a file velocity.dat in write mode
vel_file = open('velocity.dat', 'w+')

# Open a file pressure.dat in write mode
pres_file = open('pressure.dat', 'w+')

# Open a file ns.txt in write mode
nss = open('ns.txt', 'w+')

for i in range(len(fs)):
    if i > 2000:
        vel = dict([(velocity.nodeLabel, velocity.data[0]) for velocity in fs[i].fieldOutputs['V'].values])
        pre = dict([(pressure.nodeLabel, pressure.data) for pressure in fs[i].fieldOutputs['PRESSURE'].values])
        vels = list(itertools.chain(vel.values()))
        pres = list(itertools.chain(pre.values()))
        ns = list(vel.keys())
        vel_file.write('%s\n' % (str(vels)[1:-1]))
        pres_file.write('%s\n' % (str(pres)[1:-1]))

vel_file.close()
pres_file.close()
nss.write('%s\n' % (str(ns)[1:-1]))
nss.close()
