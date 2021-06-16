#!/usr/bin/env python3


import matplotlib.pyplot as plt
import argparse

def loadPoints(fileName):
    f1 = open(fileName, 'r')
    lines = f1.readlines()
    f1.close()

    loc = []
    for line in lines:
        coord = line.split(' ')
        loc.append((float(coord[0]), float(coord[1])))
    return loc

def plot(locs, radius, outName, city, density):

    x=[]
    y=[]
    circles=[]


    for loc in locs:
        x.append(loc[0])
        y.append(loc[1])
        circles.append(plt.Circle((loc[0], loc[1]), radius=radius, color='r', alpha=0.2, edgecolor=None))


    plt.title(f'Uniform random location of nodes with a population density\nof {density} people / km^2 in {city} with a {radius}m wifi coverage')
    plt.xlabel("x location (m)")
    plt.ylabel("y location (m)")
    plt.scatter(x, y, color='r', s=5)
    ax = plt.axis([-1,5001,-1,5001])
    plt.gcf().gca().set_aspect('equal')
    for circle in circles:
        plt.gcf().gca().add_artist(circle)
    plt.savefig(outName, dpi=600)


if __name__== '__main__':

    parser = argparse.ArgumentParser(description="make some charts")
    parser.add_argument('fileName', type=str, metavar='FILE', help="The file name to parse")
    parser.add_argument('--range', type=int, help="the range in meters of the wifi coverage", default=50)
    parser.add_argument('--city', type=str, help="the name of the city that is being plotted", required=True)
    parser.add_argument('--density', type=float, help="population density", required=True)
    args = parser.parse_args()

    outName = args.fileName.split('.')[0] + '.png'

    print(args)
    locations = loadPoints(args.fileName)
    plot(locations, args.range, outName, args.city, args.density)
