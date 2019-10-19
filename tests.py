from server import *
import math

def test_calculate_distance():
	X1, Y1 = 0, 0
	X2, Y2 = 5, 5
	assert(calculate_distance(X1, Y1, X2, Y2) == math.sqrt(50))
	
test_calculate_distance()