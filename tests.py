from server import *
import math

def test_calculate_distance():
	X1, Y1 = 0, 0
	X2, Y2 = 5, 5
	expected = math.sqrt(50) 
	actual = calculate_distance(X1, Y1, X2, Y2)
	assert(actual == expected)

def test_equidistant_points():
	X1, Y1 = 1, 1
	X2, Y2 = 5, 5
	parts = 4
	expectedX, expectedY =  [1.0, 2.0, 3.0, 4.0, 5.0], [1.0, 2.0, 3.0, 4.0, 5.0]
	actualX, actualY = get_equidistant_points(X1, Y1, X2, Y2, parts)
	assert(actualX == expectedX)   
	assert(actualY == expectedY)   


def test_path_length():
	points_X, points_Y = [1.0, 2.0, 3.0, 4.0, 5.0], [1.0, 2.0, 3.0, 4.0, 5.0]
	expected = 4*math.sqrt(2)
	actual = find_path_length(points_X, points_Y)
	assert(actual == expected)

def test_generate_sample_points():
	# the
	# points_X = [170, 225, 100]
	# points_Y = [50, 85, 50]

	# #venue
	points_X = [170, 100, 240, 240, 100]
	points_Y = [120, 50, 120, 50, 50]

	sample_points_X, sample_points_Y = generate_sample_points(points_X, points_Y)
	
	assert(len(sample_points_X) == len(sample_points_Y))
	assert(len(sample_points_X) == 100)
	
	# path_length = find_path_length(points_X, points_Y)
	# print(path_length)
	# expected_distance = round(path_length/99, 2)
	# print(expected_distance)

	# for index in range(99):
	# 	currentX, currentY = sample_points_X[index], sample_points_Y[index]
	# 	nextX, nextY = sample_points_X[index + 1], sample_points_Y[index + 1]
	# 	print(calculate_distance(currentX, currentY, nextX, nextY))


test_path_length()
test_equidistant_points()
test_calculate_distance()
test_generate_sample_points()