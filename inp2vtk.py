# Script to convert inp file to vtk file

def status(string):
    print("-" * 30)
    print(string)


inp = open('vort_shedding.inp', 'r')
vtk = open('vort_shedding.vtk', 'w')

vtk.write("# vtk DataFile Version 3.0\n")
vtk.write("Mesh Data Information\n")
vtk.write("ASCII\n")
vtk.write("DATASET UNSTRUCTURED_GRID\n\n")

# READ DATA FROM INP FILE
status("READING INP FILE")

lines = inp.readlines()

# CREATING A LIST OF COORDINATES
nodal_data = []

nodal_flag = False
for i in range(len(lines)):
    if nodal_flag:
        nodal_data.append(lines[i])
    if lines[i] == '*Node\n':
        nodal_flag = True
    if lines[i] == '*Element, type=FC3D8\n':
        nodal_flag = False
        nodal_data.remove('*Element, type=FC3D8\n')

status("WRITING COORDINATES TO VTK")

nodes = []
for node in nodal_data:
    nodes.append(node.replace(' ', '').replace('\n', '').split(','))

num_nodes = len(nodes)
vtk.write("POINTS {} float\n".format(num_nodes))

for node in nodes:
    vtk.write("{0} {1} {2}\n".format(node[1], node[2], node[3]))

# CONNECTIVITY
conn_data = []

conn_flag = False
for i in range(len(lines)):
    if conn_flag:
        conn_data.append(lines[i])
    if '*Element' in lines[i]:
        conn_flag = True
    if "*Nset" in lines[i]:
        conn_flag = False

status("WRITING ELEMENT CONNECTIVITY DATA TO VTK")

elements = []
for connectivity in conn_data[:-1]:
    elements.append(connectivity.replace(' ', '').replace('\n', '').split(','))

num_elem = len(elements)
vtk.write("\nCELLS {0} {1}\n".format(num_elem, num_elem * 9))

# SUBTRACT ONE FROM EACH NODE NUMBER TO START THE NUMBERING FROM ZERO
for element in elements:
    vtk.write(
        "8 {0} {1} {2} {3} {4} {5} {6} {7}\n".format(eval(element[1]) - 1, eval(element[2]) - 1, eval(element[3]) - 1,
                                                     eval(element[4]) - 1, eval(element[5]) - 1,
                                                     eval(element[6]) - 1, eval(element[7]) - 1, eval(element[8]) - 1))

status("WRITING CELL TYPE TO VTK")

vtk.write('\n')
vtk.write("CELL_TYPES {}\n".format(num_elem))
for i in range(len(elements)):
    vtk.write("12\n")

status("READING VELOCITY POD MODAL DATA")

vel_pod_data = open('v_pod_modes.txt', 'r')
vel_pod_raw = vel_pod_data.readlines()
vel_pod_loc = []
for vel_pod_row in vel_pod_raw:
    vel_pod_loc.append(vel_pod_row.replace(' ', '').replace('\n', '').split(','))

status("WRITING VELOCITY POD MODAL DATA TO VTK")
vtk.write('\nPOINT_DATA {}\n'.format(num_nodes))

for mode in range(10):
    if mode + 1 < 10:
        vtk.write('\nSCALARS vel_POD_mode_0{} float 1\n'.format(mode + 1))
    else:
        vtk.write('\nSCALARS vel_POD_mode_{} float 1\n'.format(mode + 1))

    vtk.write('LOOKUP_TABLE default\n')
    for node in vel_pod_loc:
        vtk.write(node[mode] + '\n')

vel_pod_data.close()

status("READING VELOCITY DMD MODAL DATA")

vel_dmd_data = open('v_dmd_modes.txt', 'r')
vel_dmd_raw = vel_dmd_data.readlines()
vel_dmd_loc = []
for vel_dmd_row in vel_dmd_raw:
    vel_dmd_loc.append(vel_dmd_row.replace(' ', '').replace('\n', '').split(','))

status("WRITING VELOCITY DMD MODAL DATA TO VTK")

for mode in range(20):
    # since dmd modes are in pairs because of complex conjugate nature, we only take one of the two
    # if mode % 2 == 0:
    #     if (((mode + 1) + 1)/2) < 10:
    #         vtk.write('\nSCALARS vel_DMD_mode_0{} float64 1\n'.format(int(((mode + 1) + 1) / 2)))
    #     else:
    #         vtk.write('\nSCALARS vel_DMD_mode_{} float64 1\n'.format(int(((mode + 1) + 1) / 2)))
    vtk.write('\nSCALARS vel_DMD_mode_{} float64 1\n'.format(mode))
    vtk.write('LOOKUP_TABLE default\n')
    for node in vel_dmd_loc:
        vtk.write(node[mode] + '\n')

vel_dmd_data.close()

status("READING PRESSURE POD MODAL DATA")

p_pod_data = open('p_pod_modes.txt', 'r')
p_pod_raw = p_pod_data.readlines()
p_pod_loc = []
for p_pod_row in p_pod_raw:
    p_pod_loc.append(p_pod_row.replace(' ', '').replace('\n', '').split(','))

status("WRITING PRESSURE POD MODAL DATA TO VTK")

for mode in range(10):
    if mode + 1 < 10:
        vtk.write('\nSCALARS p_POD_mode_0{} float 1\n'.format(mode + 1))
    else:
        vtk.write('\nSCALARS p_POD_mode_{} float 1\n'.format(mode + 1))

    vtk.write('LOOKUP_TABLE default\n')
    for node in p_pod_loc:
        vtk.write(node[mode] + '\n')

p_pod_data.close()

status("READING PRESSURE DMD MODAL DATA")

p_dmd_data = open('p_dmd_modes.txt', 'r')
p_dmd_raw = p_dmd_data.readlines()
p_dmd_loc = []
for p_dmd_row in p_dmd_raw:
    p_dmd_loc.append(p_dmd_row.replace(' ', '').replace('\n', '').split(','))

status("WRITING PRESSURE DMD MODAL DATA TO VTK")

for mode in range(10):
    # since dmd modes are in pairs because of complex conjugate nature, we only take one of the two
    if mode % 2 == 0:
        if (((mode + 1) + 1)/2) < 10:
            vtk.write('\nSCALARS p_DMD_mode_0{} float 1\n'.format(int(((mode + 1) + 1) / 2)))
        else:
            vtk.write('\nSCALARS p_DMD_mode_{} float 1\n'.format(int(((mode + 1) + 1) / 2)))

        vtk.write('LOOKUP_TABLE default\n')
        for node in p_dmd_loc:
            vtk.write(node[mode] + '\n')

p_dmd_data.close()

vtk.close()
inp.close()
