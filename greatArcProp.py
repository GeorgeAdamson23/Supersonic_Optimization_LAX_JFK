# George Adamson
# 05/19/2020

fhand1 = open('dijkstraRoute_oceanEN_RD_50km_50.txt')
fhand_out = open('dijkstraRoute_oceanEN_RD_50km_50.pg','w')

# Read in Route
lats = []
lons = []
for line in fhand1:
    route_data = line.split(',')
    lats.append(route_data[1])
    lons.append(route_data[2].rstrip())

# Header Information
fhand_out.write('stk.v.11.7')
fhand_out.write('\n\tBEGIN GreatArc')
fhand_out.write('\n\t\tMethod DetTimeAccFromVel')
fhand_out.write('\n\t\tTimeOfFirstWaypoint 19 May 2020 16:00:00.000000000')
fhand_out.write('\n\t\tArcGranularity 5.729577951308e-001')
fhand_out.write('\n\t\tAltRef WGS84')
fhand_out.write('\n\t\tAltInterpMethod EllipsoidHeight')
fhand_out.write('\n\t\tNumberOfWaypoints 29')
fhand_out.write('\n\t\tBEGIN Waypoints')

for i in range(0,len(lats)):

    time = i * 1.016507057765e4
    alt = 18288.00000

    fhand_out.write('\n\t\t' + str(time) + " " + str(lats[i]) + " " + str(-1*float(lons[i])) + " " + str(alt) + " " + str(0.59944444444444) + " " + str(0.000000000000e0))


fhand_out.write('\n\t\tEND Waypoints')
fhand_out.write('\n\tEND GreatArc')


# Close Files
fhand1.close()
fhand_out.close()
