import csv
import math
import random
import sys
import time
from statistics import mean, variance

import numpy as np
import pygame




class ElectionResultsCity:
    def __init__(self, _city_name, _economics):
        self.city_name = _city_name
        self.economics = _economics
        self.total_votes = None
        self.row_data_array = None
        self.vector = None

class HexagonData:
    def __init__(self, _vector):
        self.vector = _vector
        self.position_to_draw = None
        self.color = None
        self.economics = []
        self.accuracy = None
        self.first_neighbours = set()
        self.second_neighbours = set()
        self.associated_cities = set()



# return vector of city votes values(normal) and the first value is a economics
def get_normal_vector(economics, total_votes, vector_votes):

    if add_economic:
        return_vector = [economics / 10]
    else:
        return_vector = []
    for party in vector_votes:
        return_vector.append(party/total_votes)

    return np.array(return_vector)

#get data from csv and init
def data_from_csv():
    file = open('Elec_24.csv')
    city_classes.clear()
    csvreader = csv.reader(file)
    #next header
    next(csvreader)

    for row in csvreader:
        city_class = ElectionResultsCity(row[0], int(row[1]))

        vector = []
        for i in range(3, len(row)):
            vector.append(int(row[i]))
        city_class.row_data_array = vector
        city_class.total_votes = sum(vector)
        city_class.vector = get_normal_vector(city_class.economics, city_class.total_votes, city_class.row_data_array)

        city_classes[city_class.city_name] = city_class

# return vector with andom values between 0-1
def get_random_values_vector(num_of_values=13):
    row_values = []
    for i in range(num_of_values):
        random.seed(time.time())
        row_values.append(random.randint(0, 1000000))
    sum_values = sum(row_values)

    return_vector = []
    if add_economic:
        return_vector = [random.randint(1, 10)/10]

    for value in row_values:
        return_vector.append(value/sum_values)
    return np.array(return_vector)

#get position with distance 2
def get_second_neighbours(pos):
    second_neighbours_delta_odd_row = [(-2, 0), (-2, 1), (-2, -1), (-1, -2), (-1, 1), (0, -2), (0, 2), (1, -2), (1, 1), (2, 0), (2, 1), (2, -1)]
    second_neighbours_delta_even_row = [(-2, 0), (-2, 1), (-2, -1), (-1, -1), (-1, 2), (0, -2), (0, 2), (1, -1), (1, 2), (2, 0), (2, 1), (2, -1)]
    second_neighbours = set()

#seperate between odd and even rows

    if (pos[0] % 2) == 0:
        for delta in second_neighbours_delta_even_row:
            temp_neighbour = (pos[0] + delta[0], pos[1] + delta[1])
            if temp_neighbour in positions:
                second_neighbours.add(temp_neighbour)

    if (pos[0] % 2) == 1:
        for delta in second_neighbours_delta_odd_row:
            temp_neighbour = (pos[0] + delta[0], pos[1] + delta[1])
            if temp_neighbour in positions:
                second_neighbours.add(temp_neighbour)

    return second_neighbours

def get_first_neighbours(pos):
    neighbours_delta_odd_row = [(-1, 0), (-1, -1), (0, -1), (0, 1), (1, 0), (1, -1)]
    neighbours_delta_even_row = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    first_neighbours = set()

    if (pos[0] % 2) == 0:
        for delta in neighbours_delta_even_row:
            temp_neighbour = (pos[0] + delta[0], pos[1] + delta[1])
            if temp_neighbour in positions:
                first_neighbours.add(temp_neighbour)

    if (pos[0] % 2) == 1:
        for delta in neighbours_delta_odd_row:
            temp_neighbour = (pos[0] + delta[0], pos[1] + delta[1])
            if temp_neighbour in positions:
                first_neighbours.add(temp_neighbour)

    return first_neighbours

# calculate the position to draw the grid
def get_position_to_draw(pos):

    if pos[0]%2 == 0:
        x = x_start + pos[1] * x_shift_inline + x_shift_inline/2
    else:
        x = x_start+pos[1]*x_shift_inline

    y = y_start+pos[0]*y_shift
    return x, y

# get color for each hexagon
def get_color_hexagon(city_economics):
    if not city_economics:
        return color_empty

    avg_economics = sum(city_economics)/len(city_economics)
    if 1 <= avg_economics < 2:
        return color1
    elif 2 <= avg_economics < 3:
        return color2
    elif 3 <= avg_economics < 4:
        return color3
    elif 4 <= avg_economics < 5:
        return color4
    elif 5 <= avg_economics < 6:
        return color5
    elif 6 <= avg_economics < 7:
        return color6
    elif 7 <= avg_economics < 8:
        return color7
    elif 8 <= avg_economics < 9:
        return color8
    elif 9 <= avg_economics:
        return color9


def draw_board():

    for hexagon in hexagons.values():
        draw_regular_polygon(surface, get_color_hexagon(hexagon.economics), 6, size,
                             hexagon.position_to_draw)

#init hexagons with random values
def initialize_values():
    hexagons.clear()
    init_values = [[2, 3, 4, 5, 6],
                  [2, 3, 4, 5, 6, 7],
                  [1, 2, 3, 4, 5, 6, 7],
                  [1, 2, 3, 4, 5, 6, 7, 8],
                  [0, 1, 2, 3, 4, 5, 6, 7, 8],
                  [1, 2, 3, 4, 5, 6, 7, 8],
                  [1, 2, 3, 4, 5, 6, 7],
                  [2, 3, 4, 5, 6, 7],
                  [2, 3, 4, 5, 6]]


    r = 0
    for line in init_values:
        for col in line:
            positions.append((r, col))
        r += 1

    #init the hexagon data
    for pos in positions:
        new_hexagon = HexagonData(get_random_values_vector())
        new_hexagon.first_neighbours = get_first_neighbours(pos)
        new_hexagon.second_neighbours = get_second_neighbours(pos)
        new_hexagon.position_to_draw = get_position_to_draw(pos)
        hexagons[pos] = new_hexagon

#return the position of nearest hexagon
def get_nearest_hexagon(city_vector):
    min_distance = sys.float_info.max
    position_nearest_hexagon = (0, 0)
    for hexagon_key in hexagons.keys():
        distance = np.linalg.norm(city_vector-hexagons.get(hexagon_key).vector)
        if distance <= min_distance:
            min_distance = distance
            position_nearest_hexagon = hexagon_key
    return position_nearest_hexagon, min_distance

#calculate delta between two vectors and appr
def update_hexagon_vector(hexagon_pos_to_update, vector_source, factor):
    nearest_hexagon_vector = hexagons.get(hexagon_pos_to_update).vector
    diff = np.subtract(vector_source, nearest_hexagon_vector) * factor
    new_vector = np.add(nearest_hexagon_vector, diff)
    hexagons.get(hexagon_pos_to_update).vector = new_vector

#calculate the score of accuracy, return the average of hexagons accuracy
def calculate_accuracy(hexagon_data):
    if not hexagon_data.economics:
        return -1
    distances = []
    for city_name in hexagon_data.associated_cities:
        distances.append(np.linalg.norm(city_classes.get(city_name).vector - hexagon_data.vector))
    return mean(distances)


def clear_all_hexagon_cities_associated():
    for hexagon in hexagons.values():
        hexagon.associated_cities.clear()
        hexagon.economics.clear()

#the main iterator. EPOCH
def iterator(values):

    clear_all_hexagon_cities_associated()

    #if shuffle flag is true --> shuffle the order of cities.
    if shuffle_cities:
        keys = list(city_classes.keys())
        random.shuffle(keys)
    else:
        keys = city_classes.keys()

    #for each city, search the nearest hexagon in grid, and update the vector
    for city_key in keys:
        city_data = city_classes.get(city_key)
        nearest_hexagon_data = get_nearest_hexagon(city_data.vector)
        nearest_hexagon = hexagons.get(nearest_hexagon_data[0])
        nearest_hexagon.associated_cities.add(city_data.city_name)
        nearest_hexagon.economics.append(city_data.economics)
        update_hexagon_vector(nearest_hexagon_data[0], city_data.vector, values[0])

        #update neighbours
        for first_neighbour in nearest_hexagon.first_neighbours:
            update_hexagon_vector(first_neighbour, city_data.vector, values[1])
        for second_neighbour in nearest_hexagon.second_neighbours:
            update_hexagon_vector(second_neighbour, city_data.vector, values[2])

    #calculate average of all accuracy
    hexagons_accuracy = []
    for hexagon in hexagons.values():
        hexagon.accuracy = calculate_accuracy(hexagon)
        if hexagon.accuracy > 0:
            hexagons_accuracy.append(hexagon.accuracy)

    avg_accuracy = mean(hexagons_accuracy)
    return avg_accuracy



def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * math.cos(math.pi / 2 + 2 * math.pi * i / n), y + r * math.sin(math.pi / 2 + 2 * math.pi * i / n))
        for i in range(n)
    ], width)



black = (0, 0, 0)
white = (235, 245, 251)
color_empty = (214, 234, 248)
color9 = (214, 234, 248)
color8 = (174, 214, 241)
color7 = (133, 193, 233)
color6 = (93, 173, 226)
color5 = (52, 152, 219)
color4 = (46, 134, 193)
color3 = (40, 116, 166)
color2 = (33, 97, 140)
color1 = (27, 79, 114)
X = 400
Y = 400

city_classes = {}
hexagons = {}
positions = []

pygame.init()
surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Drawing')
surface.fill(white)

x_start = 40
y_start = 80
size = 20
x_shift = math.cos(math.radians(30)) * size
x_shift_inline = math.cos(math.radians(30)) * size + size
y_shift = math.sin(math.radians(30)) * size + size


def run(values):
    while True:

        for i in range(10):
            avg_accuracy_list.append(iterator(values))

            draw_board()
            pygame.display.update()
            time.sleep(1)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Accuracy = ' + str(round(mean(avg_accuracy_list), 3)), True, black, white)
        textRect = text.get_rect()
        textRect.center = (200, 20)
        surface.blit(text, textRect)
        draw_board()
        pygame.display.update()

        time.sleep(300)
        pygame.quit()
        exit()

shuffle_cities = False
add_economic = False

approximation_values = [(0.30, 0.20, 0.10)]

avg_accuracy_list = []

for values in approximation_values:

    initialize_values()
    data_from_csv()
    avg_accuracy_list.append(run(values))












