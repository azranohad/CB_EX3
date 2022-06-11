import csv
import math
import random
import sys

import numpy as np
import pygame

class ElectionResultsCity:
    def __init__(self, _city_name, _economics):
        self.city_name = _city_name
        self.economics = _economics
        self.total_votes = None
        self.row_data_array = None
        self.vector = None


# return vector of city votes values(normal) and the first value is a economics
def get_normal_vector(economics, total_votes, vector_votes):
    return_vector = [economics/10]
    for party in vector_votes:
        return_vector.append(party/total_votes)

    return np.array(return_vector)


def data_from_csv():
    file = open('Elec_24.csv')
    csvreader = csv.reader(file)

    # r for skip the header
    r = 0
    for row in csvreader:
        if r > 0:
            city_class = ElectionResultsCity(row[0], int(row[1]))

            vector = []
            for i in range(3, len(row)):
                vector.append(int(row[i]))
            city_class.row_data_array = vector
            city_class.total_votes = sum(vector)
            city_class.vector = get_normal_vector(city_class.economics, city_class.total_votes, city_class.row_data_array)

            city_classes.append(city_class)

        r += 1
def get_random_values_vector(num_of_values = 13):
    row_values = []
    for i in range(num_of_values):
        row_values.append(random.randint(0, 10000))
    sum_values = sum(row_values)

    return_vector = [random.randint(1, 10)/10]
    for value in row_values:
        return_vector.append(value/sum_values)

    return np.array(return_vector)

def init_vector_values(num_of_values=15):
    col_in_row = [5, 6, 7, 8, 9, 8, 7, 6, 5]
    positions = []
    r = 0
    for num_of_col in col_in_row:
        for i in range(num_of_col):
            positions.append((r, i))
        r += 1

    for pos in positions:
        octagons[pos] = get_random_values_vector()

def get_nearest_octagon(city_vector):
    min_distance = sys.float_info.max
    position_nearest_octagon = (0, 0)
    for octagon_key in octagons.keys():
        distance = np.linalg.norm(city_vector-octagons.get(octagon_key))
        if distance < min_distance:
            min_distance = distance
            position_nearest_octagon = octagon_key

    return position_nearest_octagon, min_distance

def iterator():
    for city in city_classes:
        nearest_octagon = get_nearest_octagon(city.vector)
        y = 6
    x = 5

def draw(name):
    x = 3

def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * math.cos(math.pi / 2 + 2 * math.pi * i / n), y + r * math.sin(math.pi / 2 + 2 * math.pi * i / n))
        for i in range(n)
    ], width)


city_classes = []
octagons = {}

data_from_csv()
init_vector_values()
iterator()
