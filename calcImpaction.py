# George Adamson
# 08/14/2020

# This script determines the number of people impacted by sonic booms on an
# STK-modeled flight route. Specify a (.csv) from STK and a population
# data file (.txt).

import csv

# Input Files
fileName = 'FigureOfMerit1_Value_By_Grid_Point_Canada.csv'
fhand1 = open('popData_USCanMexBahaCuba.txt')

# The first line number (in Excel) that is not part of the header
endOfHeader = 24;

# Output File of Impacted Grid Points
file = open('temp.txt','w')

count = 1;

with open(fileName) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    data = list(readCSV)
    rowCount = len(data)

    for row in data:

        # Skip past the header information and conclude at end of CSV file
        if count >= endOfHeader and count < rowCount:
            # Only keep track of impacted grid points
            if row[2] == '1.000000':

                # Row[1] (the longitude) is in a different format than it
                # appers in other parts of this project.
                longitude = float(row[1])-360;
                if (longitude < 0):
                    longitude = longitude*-1

                # Write lat, lon, and impaction value to output file
                file.write(row[0] + "," + ('%.6f' % longitude) + "," + row[2])
                file.write("\n")

        count = count+1

file.close()

fhand2 = open('temp.txt')

lats = []
lons = []
pop = []
datasetPop = 0;
for line in fhand1:
    data = line.split(',')
    lats.append(data[0])
    lons.append(data[1])
    pop.append(data[2].rstrip())
    datasetPop += float(data[2])


totalPop = 0
counter = 0

for line in fhand2:

    counter += 1

    data = line.split(',')
    im_lat = data[0]
    im_lon = data[1]

    lat_index = lats.index(im_lat)
    lon_index = lons.index(im_lon, lat_index, -1)

    if lat_index != lon_index:

        lat_index = [i for i, n in enumerate(lats) if n == im_lat]
        lon_index = [i for i, n in enumerate(lons) if n == im_lon]

        common_index = list(set(lat_index).intersection(lon_index))[0]

        totalPop += float(pop[common_index])

    else:
        totalPop += float(pop[lat_index])

    if (counter % 100 == 0): print(str(counter) + ' Entries Completed.')

print('\nPopulation Impacted: ', totalPop)
print('Total Population: ', datasetPop)
print('Impaction: ', totalPop/datasetPop)
