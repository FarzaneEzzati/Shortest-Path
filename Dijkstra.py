import numpy as np
import random as random
import math
import pickle
import matplotlib.pyplot as plt


class Network:
    def __init__(self, network):
        self.tvt = network

    def getDijTable(self, nodes, origin):
        # initialization step
        M = np.max(self.tvt)
        UV = [origin]
        for point in nodes:
            if point != origin:
                UV.append(point)
        Dij = [UV.copy(), [M for i in UV], [0 for i in UV]]
        Dij[1][0] = 0
        C_index = origin  # to avoid error: reference before assignment
        C = 0

        # Condition 1
        while len(UV) > 1:

            # Find the node from UV with the minimum distance from origin
            min_distance = M
            for node in range(len(Dij[0])):
                if (Dij[0][node] in UV) and (Dij[1][node] <= min_distance):
                    min_distance = Dij[1][node]
                    C = Dij[0][node]
                    C_index = node
            # output: C as the selected node

            # Find all connections with C from UV
            # tt_from_C shows the travel time from C to each node in UV
            # if UV = [3, 5, 7], and tt_from_C = [12, M, 6],
            # then travel time from C to 3 is 12, to 5 is infeasible, and to 7 is 6'''
            tt_from_C = [self.tvt[C][i] for i in UV]
            # output: distance from C to unvisited nodes

            # For each feasible connection, find the path through C
            # Compare it with the current shortest path to each UV node
            for i in range(len(UV)):
                if tt_from_C[i] < M:
                    # There is a feasible path
                    new_path = Dij[1][C_index] + tt_from_C[i]
                    current_path = Dij[1][Dij[0].index(UV[i])]
                    if new_path <= current_path:
                        # New shortest path. Update Dij
                        Dij[1][Dij[0].index(UV[i])] = new_path
                        Dij[2][Dij[0].index(UV[i])] = C
            UV.remove(C)
        return Dij

    def getPath(self, dij, destination):
        p = [destination]
        traveler = destination
        traveltime = dij[1][dij[0].index(destination)]

        # find the path using dij
        while traveler != dij[0][0]:
            traveler_index = dij[0].index(traveler)
            p.append(dij[2][traveler_index])
            traveler = dij[2][traveler_index]

        return p[::-1], traveltime


if __name__ == '__main__':
    network_data = [[500, 2, 4, 6, 8],
                    [2, 500, 1, 500, 500],
                    [4, 1, 500, 1, 3],
                    [6, 500, 1, 500, 1],
                    [8, 500, 3, 1, 500]]
    sp = Network(network_data)

    # testing the functions in Shortest Path class
    start = 4  # origin
    finish = 0  # destination

    Dij0 = sp.getDijTable(range(5), start)  # gets the nodes and the origin, return the Dij table
    path, travel_time = sp.getPath(Dij0, finish)  # gets Dij and destination, returns the shortest path and distance

    print(f'Path from {start} to {finish} is {path} with travel time {travel_time}\n')
    print(f'Dij Table: {Dij0}')
