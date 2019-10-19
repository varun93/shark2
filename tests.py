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
	pass

test_path_length()
test_equidistant_points()
test_calculate_distance()