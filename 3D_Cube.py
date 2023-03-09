import pygame # imports 
import numpy as np
from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100 # scale set for ouput on display

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y. Also has centering for cube in middle of render. 

angle = 0 # rotation variable that feeds into the rotation matrix 

points = [] # empty array 

# all the cube vertices
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

# The vertices (x,y,z) will be projected to the x,y vertices by the prjection layer matrix 

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points): # function for connection of points on square 
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


clock = pygame.time.Clock()
while True:

    clock.tick(60) # fps limit of plugin. 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


    rotation_z = np.matrix([  # update stuff, using the rotation exmaple provided, this uses the rotation equation from rotation z. 
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([ # rotation y 
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([ # rotation x 
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    angle += 0.01

    screen.fill(WHITE)
    # drawining stuff

    i = 0
    for point in points: 
        rotated2d = np.dot(rotation_z, point.reshape((3, 1))) # applying a new multiplication to the rotation2d variable 
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        # np.dot is a matrix multiplication. Reshape fucntion converts the 1D array into a 2D array. 

        projected2d = np.dot(projection_matrix, rotated2d) 

        x = int(projected2d[0][0] * scale) + circle_pos[0] # x & y variables converted into a int, (0,0) represents the x value of the cube, for every x point, there is an ascociated z and y value. 
        y = int(projected2d[1][0] * scale) + circle_pos[1] # circle position for each corner of the square 

        projected_points[i] = [x, y] # this version of X and Y would be the versions of the porjections for the 2D variable in a 2D array, so that i can be multiplied later. 
        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    for p in range(4): # for loop to connect all points of cube using function.
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    pygame.display.update()
