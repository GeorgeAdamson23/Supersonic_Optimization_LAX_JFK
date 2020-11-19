# George Adamson
# 01/21/2020

# Reformats waypoints generated from the following link:
# http://navaid.com/GPX/

#from bs4 import BeautifulSoup

#fhand = open('0ecb6fd7.gpx')
fhand = open('74206.gpx')

waypointList = []
currentWaypoint = ["Name","Lat","Lon","State","Country","Comment"]

for line in fhand:
    line = line.rstrip()

    if line.startswith('<navaid:name>'):
        name = (line.split('<navaid:name>')[1]).split('</navaid:name>')[0]
        currentWaypoint[0] = name;

    if line.startswith('<wpt lat'):

        latAndLon = line
        lat = latAndLon.split('"')[1]
        lon = latAndLon.split('"')[3]

        # Get rid of the negative sign on the longitude
        if lon.startswith('-'):
            lon = lon[1:]

        currentWaypoint[1] = lat;
        currentWaypoint[2] = lon;

    if line.startswith('<navaid:state>'):
        state = (line.split('<navaid:state>')[1]).split('</navaid:state>')[0]
        currentWaypoint[3] = state;

    if line.startswith('<navaid:country>'):
        country = (line.split('<navaid:country>')[1]).split('</navaid:country>')[0]
        currentWaypoint[4] = country;

    if line.startswith('<cmt>'):
        comment = (line.split('<cmt>')[1]).split('</cmt>')[0]
        currentWaypoint[5] = comment;

    #End of current waypoint. Add to list of waypoints and reset the list
    if line.startswith('</wpt>'):
        #print(currentWaypoint)
        waypointList.append(currentWaypoint)
        currentWaypoint = ["Name","Lat","Lon","State","Country","Comment"]

    continue

print(len(waypointList))

file = open('waypoints_74206.txt','w')
for waypoint in waypointList:
    file.write(waypoint[0] + "," + waypoint[1] + "," + waypoint[2] + "," + waypoint[3] + "," + waypoint[4] + "," + waypoint[5])
    file.write("\n")
    
print('done')
