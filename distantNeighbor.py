# George Adamson
# 05/08/2020

# This script calculates k distant neighbors for each waypoint in the dataset.
# Distant refers to each neighbor required to be of distance X away from
# the "parent" waypoint.

import math
from heapq import heappop, heappush, heapify
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# Only keep track of k nearest neighbors
capacity = 20

count = 0

# Input File
fhand = open('waypoints_oceanEN.txt')
# Output File
file = open('neighborWaypoints_oceanEN_100km_20.txt','w')

lats = []
lons = []

for line in fhand:
    waypointData = line.split(",")
    lats.append(waypointData[0])
    lons.append(waypointData[1])

for i in range(0, len(lats)):

    # Create empty heap
    heap = []
    heapify(heap)

    p1_lat = float(lats[i])
    p1_lon = float(lons[i])


    for j in range(0, len(lats)):

        if i != j:

            p2_lat = float(lats[j])
            p2_lon = float(lons[j])

            distance = haversine(p1_lon,p1_lat,p2_lon,p2_lat)

            # A good rule of thumb is 200km over the minimum
            if distance < 100 or distance > 300: continue

            if len(heap) < capacity:
                heappush(heap, (-1*distance,j) )
            else:
                # Equivalent to a push, then a pop, but faster
                heappush(heap, (-1*distance,j) )
                heappop(heap)


    file.write(str(p1_lat) + "," + str(p1_lon))
    for k in heap:
        file.write("," + str(k[1]))
    file.write("\n")

    count+=1

    if count % 100 == 0:
        print(count, ' Completed')

    if count == len(lats):
        print('Done')

    if i == (len(lats)-1) and len(heap) == 0:
        print('WARNINING: No Neighbors')

file.close()
