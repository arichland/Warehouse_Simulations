_author_ = 'arichland'

import numpy as np
import pandas as pd
from ast import literal_eval

# Calculate Picker Route Distance between two locations
def distance_picking(Loc1, Loc2, y_low, y_high):

    # Start Point
    x1, y1 = int(Loc1[0]), int(Loc1[1])

    # End Point
    x2, y2 = int(Loc2[0]), int(Loc2[1])

    # Distance x-axis
    distance_x = abs(x2 - x1)

    # Distance y-axis
    if x1 == x2:
        distance_y1 = abs(y2 - y1)
        distance_y2 = distance_y1
    else:
        distance_y1 = (y_high - y1) + (y_high - y2)
        distance_y2 = (y1 - y_low) + (y2 - y_low)

    # Minimum distance on y-axis
    distance_y = min(distance_y1, distance_y2)

    # Total distance
    distance = distance_x + distance_y

    return distance


def next_location(start_loc, list_locs, y_low, y_high):
    # Distance to every next points candidate
    list_dist = [distance_picking(start_loc, i, y_low, y_high) for i in list_locs]

    # Minimum Distance
    distance_next = min(list_dist)

    # Location of minimum distance
    index_min = list_dist.index(min(list_dist))
    next_loc = list_locs[index_min]  # Next location is the first location with distance = min (**)
    list_locs.remove(next_loc)  # Next location is removed from the list of candidates
    print(list_locs, "start=", start_loc, "next=", next_loc, "distance to next pick=", distance_next)

    return list_locs, start_loc, next_loc, distance_next


def create_picking_route(origin_loc, list_locs, y_low, y_high):
    # Total distance variable
    wave_distance = 0

    # Current location variable
    start_loc = origin_loc

    # Store routes
    list_chemin = []
    list_chemin.append(start_loc)

    while len(list_locs) > 0:  # Looping until all locations are picked
        # Going to next location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)

        # Update start_loc
        start_loc = next_loc
        list_chemin.append(start_loc)

        # Update distance
        wave_distance = wave_distance + distance_next

        # Final distance from last storage location to origin
    wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)

    return print(wave_distance, list_chemin)