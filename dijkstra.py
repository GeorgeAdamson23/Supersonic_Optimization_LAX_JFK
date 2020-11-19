# George Adamson
# 05/18/2020


# This script uses Dijkstra's algorithm to determine the aircraft route with
# the lowest population impaction by a supersonic aircraft.
# It takes in two input files.
    # waypoints.txt:
        # In the form: LATITUDE,LONGITUDE,WP_NAME,STATE,COUNTRY
    # network.txt:
        # In the form: WP, NEAREST_NEIGHBOR1, NEIGHBOR1_WEIGHT, etc. for 10 neighbors total
# It outputs to one file:
    # dijkstraRoute.txt:
        # In the form: WP_NAME,LATITUDE,LONGITUDE

# Reference Video Used During Coding:
    # https://www.youtube.com/watch?v=pVfj6mxhdMw
# Contact George Adamson at geoadams@umich.edu with any questions.


import math


# Reference Waypoints:
# DOCKR = LAX
# FEDAR = JFK
# start_wp = 'DOCKR'
start_wp = 'FEYLA'
final_wp = 'FEDAR'


# Print Code Progress Reports (0 or 1)?
dispProg = 1


# Input Files
fhand1 = open('waypoints_oceanEN_RD.txt')
fhand2 = open('network_oceanEN_RD_100km_50.txt')

# Output File
fhand_out = open('dijkstraRoute_oceanEN_RD_100km_50.txt','w')


# Create list of unvisited waypoints, also note the latitude/longitude pair
# of each waypoint for reference
unvisited = []
lats = []
lons = []
for line in fhand1:

    waypointData = line.split(",")

    # Index will be waypoint name, key will be 0 for unvisited (default)
    unvisited.append(waypointData[2].rstrip())
    lats.append(waypointData[0])
    lons.append(waypointData[1])


# Store waypoints, their nearest neighbors, and the population weighting
nearest_neighbors = {};
for line in fhand2:

    neighbor = {};

    neighborData = line.split(",")

    wp = neighborData[0]

    for i in range(1,len(neighborData),2):

        NN = neighborData[i];
        weight = neighborData[i+1]

        neighbor[NN] = float(weight)

    nearest_neighbors[wp] = neighbor


# Close the input files
fhand1.close()
fhand2.close()


# Note the total number of waypoints and create a copy of the wp list for reference
num_wp = len(unvisited)
wp_ref = unvisited.copy()


# Create list of visited waypoints, empty by default
visited = []


# For each waypoint, we must keep track of the smallest weight from
# start (DOCKR) to the waypoint at hand.
# All weights are inf by default
sh_dis_st = [math.inf] * num_wp


# For each waypoint, note the previous waypoint that leads to said waypoint
# via the shortest weight
prev_wp = [None] * num_wp


# Weight from starting waypoint (DOCKR) to starting waypoint is zero
sh_dis_st[unvisited.index(start_wp)] = 0


# Create a copy of shortest weight for reference
sh_dis_st_ref = sh_dis_st.copy()


# While waypoints are unvisited,
while len(visited) < num_wp:

    # Visit an unvisited waypoint with the smallest weight from start
    wp_to_visit = unvisited[sh_dis_st.index(min(sh_dis_st))]

    # Waypoint's 10 nearest neighbors
    wp_neighbors = list(nearest_neighbors[wp_to_visit].keys())

    # Current weight from start for the wp we are visiting
    cur_dis_st = sh_dis_st_ref[wp_ref.index(wp_to_visit)]

    for i in range(0,len(wp_neighbors)):

        # Only visit unvisited neighboring waypoints
        if wp_neighbors[i] not in visited:

            # Weight from the wp we are visitng to the nearest neighbor
            im_weight = nearest_neighbors[wp_to_visit][wp_neighbors[i]]

            # If the weight from the start to the neighbor is less than the current
            # weight, we must update the shortest weight and the previous wp
            if (im_weight + cur_dis_st) < sh_dis_st_ref[wp_ref.index(wp_neighbors[i])]:

                # Note the new weight
                sh_dis_st[unvisited.index(wp_neighbors[i])] = (im_weight + cur_dis_st)
                sh_dis_st_ref[wp_ref.index(wp_neighbors[i])] = (im_weight + cur_dis_st)

                # Note the waypoint that leads to this neighbor via the shortest weight
                prev_wp[wp_ref.index(wp_neighbors[i])] = wp_to_visit

    # Waypoint is now visited, and is removed from the unvisited list
    visited.append(wp_to_visit)
    del sh_dis_st[unvisited.index(wp_to_visit)]
    unvisited.remove(wp_to_visit)

    # Print progress reports every 1000 visited waypoints
    if len(visited) % 10 == 0 and dispProg == 1:
        print(len(visited),' Entries Completed')


# Display completion
if dispProg == 1:
    print(len(visited),' Entries Completed')
    print('Done')


# Backtrack along prev_wp list to get the entire route
route = []
c_wp = final_wp

while c_wp != start_wp:

    route.append(c_wp)
    c_wp = prev_wp[wp_ref.index(c_wp)]

route.append(c_wp)

route.reverse()


# Store the latitude/longitude pair for the route
route_lats = []
route_lons = []

for route_wp in route:
    route_lats.append(lats[wp_ref.index(route_wp)])
    route_lons.append(lons[wp_ref.index(route_wp)])

route_lats = list(map(float,route_lats))
route_lons = list(map(float,route_lons))


# Output to File
for i in range(0,len(route)):
    fhand_out.write(route[i] + ',' + str(route_lats[i]) + ',' + str(route_lons[i]))
    fhand_out.write("\n")

fhand_out.close()
