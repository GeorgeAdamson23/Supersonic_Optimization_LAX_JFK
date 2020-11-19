# George Adamson
# 07/05/2020

# This script assembles a cost matrix (network file) for distant neighbor
# waypoints. It approximates the sonic boom primary carpet as a rectangle,
# and sums up all of the population centers that lie in this rectangle (between
# two waypoints, for all waypoints and neighbors).

import matplotlib.path as mplPath
import numpy as np
import math
import time
from math import radians, cos, sin, asin, sqrt

start = time.time()


def recCorners(p,q,l):

    a = [0,0]
    b = [0,0]
    c = [0,0]
    d = [0,0]


    # horizontal rectangle
    if p[0] == q[0]:
        a[0] = p[0] - l/2.0
        a[1] = p[1]

        d[0] = p[0] + l/2.0
        d[1] = p[1]

        b[0] = q[0] - l/2.0
        b[1] = q[1]

        c[0] = q[0] + l/2.0
        c[1] = q[1]

    # vertical rectangle
    elif p[1] == q[1]:
        a[1] = p[1] - l/2.0
        a[0] = p[0]

        d[1] = p[1] + l/2.0
        d[0] = p[0]

        b[1] = q[1] - l/2.0
        b[0] = q[0]

        c[1] = q[1] + l/2.0
        c[0] = q[0]


    # slanted rectangle
    else:
        # calculate slope of the side
        m = (p[0]-q[0])/(q[1]-p[1])
        # calculate displacements along axes
        dx = (l/math.sqrt(1+(m*m)))*0.5
        dy = m*dx

        a[0] = p[0] - dx
        a[1] = p[1] - dy

        d[0] = p[0] + dx
        d[1] = p[1] + dy

        b[0] = q[0] - dx
        b[1] = q[1] - dy

        c[0] = q[0] + dx
        c[1] = q[1] + dy

    return [a,b,c,d]

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

def costMatrix(inputFilename, outputFilename):


    #leng = 0.62
    leng = 0.844

    #[a,b,c,d] = recCorners([33.97141700,-104.98091700],[30.95873300,-104.90017800],leng)
    #[a2,b2,c2,d2] = recCorners([48.89499700,-98.57785600],[49.00,-97.13188900],leng)

    #[a,b,c,d] = recCorners([38.841431,-112.755786],[37.635189,-112.279414],leng)
    #[a2,b2,c2,d2] = recCorners([37.635189,-112.279414],[37.655669,-111.086822],leng)

    # Input Files
    fhand1 = open('waypoints_oceanEN_RD.txt')
    fhand2 = open('popData_USCanMexBahaCuba.txt')
    fhand3 = open(inputFilename)

    # Output File
    fhand_out = open(outputFilename,'w')


    # Read in Waypoints and Nearest Neighbors

    lats = []
    lons = []
    wp_name = []
    for line in fhand1:
        data = line.split(",")
        lats.append(float(data[0]))
        lons.append(float(data[1]))
        wp_name.append(data[2].rstrip())



    # Read in Population Data

    pop_lats = []
    pop_lons = []
    pop = []
    for line in fhand2:
        data = line.split(",")
        pop_lats.append(float(data[0]))
        pop_lons.append(float(data[1]))
        pop.append(float(data[2]))


    # Read in Neighbor Data
    wp_lats = []
    wp_lons = []
    neighbors = []
    for line in fhand3:
        data = line.split(",")
        wp_lats.append(float(data[0]))
        wp_lons.append(float(data[1]))
        neighbors.append(data[2:-1])


    # Setup Waypoint Matrix


    for i in range (0,len(wp_lats)):

        # Waypoint 1
        p1 = [wp_lats[i],wp_lons[i]]

        if i==0: fhand_out.write(wp_name[i])
        else: fhand_out.write('\n' + wp_name[i])

        for j in range (0,len(neighbors[i])):

            # Waypoint 2
            p2 = [lats[int(neighbors[i][j])],lons[int(neighbors[i][j])]]

            # Calculate distance between two waypoints
            # dist = haversine(p1[1],p1[0],p2[1],p2[0])

            #if dist < 200 or dist > 600: continue
            #if dist > 50: continue

            # Create impaction polygon between two waypoints
            [a,b,c,d] = recCorners(p1,p2,leng);
            xv = [a[0],b[0],c[0],d[0]];
            yv = [a[1],b[1],c[1],d[1]];

            totalPop = 0

            bbPath = mplPath.Path(np.array([[xv[0], yv[0]],
                         [xv[1], yv[1]],
                         [xv[2], yv[2]],
                         [xv[3], yv[3]]]))

            pointsInside = bbPath.contains_points(np.transpose(np.array([pop_lats,pop_lons])))

            pointIndicies = list(np.where(pointsInside)[0])


            totalPop = sum([pop[pointIndicies[m]] for m in range(0,len(pointIndicies))])


            if (totalPop == 0):
                totalPop = 0.01

            fhand_out.write(',' + wp_name[int(neighbors[i][j])] + ',' + str(totalPop))


        if (i % 10 == 0): print('Entry', i, ' completed. Runtime: ', time.time()-start, 'seconds.')

    fhand_out.close()


input1 = "neighborWaypoints_oceanEN_RD_25km_50.txt"
output1 = 'network_oceanEN_RD_25km_50.txt'

input2 = "neighborWaypoints_oceanEN_RD_50km_50.txt"
output2 = 'network_oceanEN_RD_50km_50.txt'

input3 = "neighborWaypoints_oceanEN_RD_75km_50.txt"
output3 = 'network_oceanEN_RD_75km_50.txt'

input4 = "neighborWaypoints_oceanEN_RD_100km_50.txt"
output4 = 'network_oceanEN_RD_100km_50.txt'

costMatrix(input1, output1)
costMatrix(input2, output2)
costMatrix(input3, output3)
costMatrix(input4, output4)
