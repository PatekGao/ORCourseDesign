import numpy as np

# 机队𝐾的组成和数量
K_PlaneTypes = ["B787-800", "B787-900", "B767-300", "A320"]

# 机型数量
k1 = 4
k2 = 6
k3 = 5
k4 = 2

flightSheet = [
    [1, 'NH969', 'HND', '10:05', 'SHA', '12:15', True],
    [2, 'NH970', 'SHA', '13:35', 'HND', '17:25', True],
    [3, 'NH967', 'HND', '21:30', 'PVG', '23:35', True],
    [4, 'NH968', 'PVG', '01:35', 'HND', '05:30', True],
    [5, 'NH919', 'NRT', '09:20', 'PVG', '11:40', True],
    [6, 'NH920', 'PVG', '13:05', 'NRT', '16:55', True],
    [7, 'NH973', 'KIX', '09:00', 'PVG', '10:35', False],
    [8, 'NH974', 'PVG', '11:35', 'KIX', '14:55', False],
    [9, 'NH961', 'HND', '08:55', 'PEK', '12:00', True],
    [10, 'NH962', 'PEK', '15:10', 'HND', '19:45', True],
    [11, 'NH955', 'NRT', '09:00', 'PEK', '12:05', False],
    [12, 'NH956', 'PEK', '14:15', 'NRT', '18:40', False],
    [13, 'NH931', 'NRT', '11:20', 'SZX', '15:10', False],
    [14, 'NH932', 'SZX', '17:00', 'NRT', '22:15', False],
    [15, 'NH965', 'HND', '11:30', 'SZX', '15:10', True],
    [16, 'NH966', 'SZX', '17:00', 'HND', '22:20', True],
    [17, 'NH927', 'NRT', '09:45', 'TAO', '12:30', False],
    [18, 'NH928', 'TAO', '13:30', 'NRT', '17:35', False],
    [19, 'NH933', 'NRT', '09:10', 'CAN', '13:05', True],
    [20, 'NH934', 'CAN', '14:15', 'NRT', '19:45', True],
    [21, 'NH929', 'NRT', '10:05', 'HGH', '12:50', False],
    [22, 'NH930', 'HGH', '13:40', 'NRT', '17:55', False],
    [23, 'NH903', 'NRT', '10:05', 'DLC', '12:15', False],
    [24, 'NH904', 'DLC', '13:15', 'NRT', '17:15', False]
]

NC = ['HND', 'SHA', 'PVG', 'NRT', 'KIX', 'PEK', 'SZX', 'TAO', 'CAN', 'HGH', 'DLC']

K = ["k1", "k2", "k3", "k4"]

# p_profits[(_l, _k)]
p_profits = {("L1", "k1"): 21612, ("L1", "k2"): 29138, ("L1", "k3"): 34676, ("L1", "k4"): 26646,
             ("L2", "k1"): 21612, ("L2", "k2"): 29138, ("L2", "k3"): 34676, ("L2", "k4"): 26646,
             ("L3", "k1"): 21612, ("L3", "k2"): 29138, ("L3", "k3"): 34676, ("L3", "k4"): 26646,
             ("L4", "k1"): 21612, ("L4", "k2"): 29138, ("L4", "k3"): 34676, ("L4", "k4"): 26646,
             ("L5", "k1"): 21612, ("L5", "k2"): 29138, ("L5", "k3"): 34676, ("L5", "k4"): 26646,
             ("L6", "k1"): 21612, ("L6", "k2"): 29138, ("L6", "k3"): 34676, ("L6", "k4"): 26646,
             ("L7", "k1"): 21612, ("L7", "k2"): 29138, ("L7", "k3"): 34676, ("L7", "k4"): 26646,
             ("L8", "k1"): 21612, ("L8", "k2"): 29138, ("L8", "k3"): 34676, ("L8", "k4"): 26646,
             ("L9", "k1"): 25032, ("L9", "k2"): 33750, ("L9", "k3"): 40165, ("L9", "k4"): 30863,
             ("L10", "k1"): 25032, ("L10", "k2"): 33750, ("L10", "k3"): 40165, ("L10", "k4"): 30863,
             ("L11", "k1"): 25032, ("L11", "k2"): 33750, ("L11", "k3"): 40165, ("L11", "k4"): 30863,
             ("L12", "k1"): 25032, ("L12", "k2"): 33750, ("L12", "k3"): 40165, ("L12", "k4"): 30863,
             ("L13", "k1"): 32292, ("L13", "k2"): 43538, ("L13", "k3"): 51813, ("L13", "k4"): 39814,
             ("L14", "k1"): 32292, ("L14", "k2"): 43538, ("L14", "k3"): 51813, ("L14", "k4"): 39814,
             ("L15", "k1"): 32292, ("L15", "k2"): 43538, ("L15", "k3"): 51813, ("L15", "k4"): 39814,
             ("L16", "k1"): 32292, ("L16", "k2"): 43538, ("L16", "k3"): 51813, ("L16", "k4"): 39814,
             ("L17", "k1"): 29493, ("L17", "k2"): 39764, ("L17", "k3"): 47323, ("L17", "k4"): 36364,
             ("L18", "k1"): 29493, ("L18", "k2"): 39764, ("L18", "k3"): 47323, ("L18", "k4"): 36364,
             ("L19", "k1"): 35067, ("L19", "k2"): 47279, ("L19", "k3"): 56265, ("L19", "k4"): 43235,
             ("L20", "k1"): 35067, ("L20", "k2"): 47279, ("L20", "k3"): 56265, ("L20", "k4"): 43235,
             ("L21", "k1"): 22724, ("L21", "k2"): 30638, ("L21", "k3"): 36461, ("L21", "k4"): 28017,
             ("L22", "k1"): 22724, ("L22", "k2"): 30638, ("L22", "k3"): 36461, ("L22", "k4"): 28017,
             ("L23", "k1"): 25116, ("L23", "k2"): 33863, ("L23", "k3"): 40299, ("L23", "k4"): 30967,
             ("L24", "k1"): 25116, ("L24", "k2"): 33863, ("L24", "k3"): 40299, ("L24", "k4"): 30967}

M = {'k1': 4, 'k2': 6, 'k3': 5, 'k4': 2}

c = {'k1': 12000, 'k2': 13000, 'k3': 17000, 'k4': 21000}

L = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15', 'L16', 'L17',
     'L18', 'L19', 'L20', 'L21', 'L22', 'L23', 'L24']
Lo = ['L7', 'L8', 'L11', 'L12', 'L13', 'L14', 'L17', 'L18', 'L21', 'L22', 'L23', 'L24']
Lm = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L9', 'L10', 'L15', 'L16', 'L19', 'L20']
Lc = ['L14', 'L16']



