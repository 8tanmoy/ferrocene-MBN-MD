#--generate the restraint file
b0 = 0.205
Kb = 4184.0
funct = 6

def get_index_array(filename):
    with open(filename ,"r") as f:
        lines = f.readlines()[1:]
    arr = []
    for line in lines:
        l1 = line.strip(r'\n')
        l1 = l1.split()
        arr += l1
    return list(map(int, arr))

idx_fe = get_index_array('index_fe.ndx')
idx_r1 = get_index_array('index_r1.ndx')
idx_r2 = get_index_array('index_r2.ndx')
idx_au = get_index_array('index_au.ndx')

#-- distance restraints for Fe-C(Cp) --
restfile = open('disre_fec.itp', 'w')
restfile.write('[ bonds ]\n')
restfile.write('; ai    aj  funct   b0  Kb\n')

beg = 0
for ife in idx_fe: 
    for iC in idx_r1[beg:beg + 5]:
        restfile.write( str(ife)    + ' ' +
                        str(iC)     + ' ' +
                        str(funct)  + ' ' +
                        str(b0)     + ' ' +
                        str(Kb)     + '\n')
    for iC in idx_r2[beg:beg + 5]:
        restfile.write( str(ife)    + ' ' +
                        str(iC)     + ' ' +
                        str(funct)  + ' ' +
                        str(b0)     + ' ' +
                        str(Kb)     + '\n')
    beg += 5
restfile.write('\n')
restfile.close()
#-- position restraints for gold --
auposre = open('posre_au.itp', 'w')
auposre.write('[ position_restraints ]\n')
for iau in idx_au:
    auposre.write(str(iau) + '\t' +
                    str(1) + '\t' +
                    '200000 200000 200000' + '\n')
auposre.close()

#-- angle restraint for c1-fe-c6 --
theta0  = 180.0 #degrees
k0      = 10000 #KJ mol-1 rad-1
angfile = open('angre_cp.itp', 'w')
angfile.write('[ angles ]\n')
angfile.write('; ai	aj	ak func theta0(deg) k0(kj mol-1 rad-2)\n')

beg = 0
for ife in idx_fe:
    for ii in range(5):
        angfile.write(str(idx_r1[beg + ii]) + ' ' + 
                        str(ife) + ' ' + 
                        str(idx_r2[beg + (ii + 3)%5]) + ' ' +
                        '1' + ' ' + 
                        str(theta0) + ' ' + str(k0) + '\n')
    beg += 5
angfile.close()