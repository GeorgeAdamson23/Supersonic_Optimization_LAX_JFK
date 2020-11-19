# George Adamson
# 08/14/2020

# Input File
fileName1 = 'popData_USCanMexBahaCuba.txt'
fhand1 = open(fileName1)

# Output File
fhand2 = open('customPoints_USCanMexBahaCuba.pnt','w')


# Read in Route
lats = []
lons = []
pop = 0
count = 0
for line in fhand1:
    route_data = line.split(',')
    lats.append(route_data[0])
    lons.append(route_data[1])
    pop += float(route_data[2])
    count += 1

# Header Information
fhand2.write('stk.v.11.7')
fhand2.write('\nBegin Pointlist')

for i in range(0,len(lats)):

    fhand2.write('\n' + str(lats[i]) + " " + str(-1*float(lons[i])))

fhand2.write('\nEnd Pointlist')

print(str(pop/count))


# Close Files
fhand1.close()
fhand2.close()
