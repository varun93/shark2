'''

You can modify the parameters, return values and data structures used in every function if it conflicts with your
coding style or you want to accelerate your code.

You can also import packages you want.

But please do not change the basic structure of this file including the function names. It is not recommended to merge
functions, otherwise it will be hard for TAs to grade your code. However, you can add helper function if necessary.

'''

from flask import Flask, request
from flask import render_template
import time
import json
import numpy
import math


app = Flask(__name__)

# Centroids of 26 keys
centroids_X = [50, 205, 135, 120, 100, 155, 190, 225, 275, 260, 295, 330, 275, 240, 310, 345, 30, 135, 85, 170, 240, 170, 65, 100, 205, 65]
centroids_Y = [85, 120, 120, 85, 50, 85, 85, 85, 50, 85, 85, 85, 120, 120, 50, 50, 50, 50, 85, 50, 50, 120, 50, 120, 50, 120]

# Pre-process the dictionary and get templates of 10000 words
words, probabilities = [], {}
template_points_X, template_points_Y = [], []
file = open('words_10000.txt')
content = file.read()
file.close()
content = content.split('\n')
for line in content:
    line = line.split('\t')
    words.append(line[0])
    probabilities[line[0]] = float(line[2])
    template_points_X.append([])
    template_points_Y.append([])
    for c in line[0]:
        template_points_X[-1].append(centroids_X[ord(c) - 97])
        template_points_Y[-1].append(centroids_Y[ord(c) - 97])



def calculate_distance(X1, Y1, X2, Y2):
    return math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)

'''
 Uniformly Sample n points between two points  
 The below function is taken from https://stackoverflow.com/questions/47443037/equidistant-points-between-two-points-in-python
 with the change in function name 
'''
def get_equidistant_points(X1, Y1, X2, Y2, parts):
    return numpy.linspace(X1, X2, parts+1), numpy.linspace(Y1, Y2, parts+1)

def find_path_length(points_X, points_Y):
    
    length = len(points_X)
    distance = 0

    for index in range(length - 1):
        current_X = points_X[index]
        current_Y = points_Y[index]
        next_X = points_Y[index + 1]
        next_Y = points_Y[index + 1]
        distance += calculate_distance(current_X, current_Y, next_X, next_Y)

    return distance

def generate_sample_points(points_X, points_Y):
    '''Generate 100 sampled points for a gesture.

    In this function, we should convert every gesture or template to a set of 100 points, such that we can compare
    the input gesture and a template computationally.

    :param points_X: A list of X-axis values of a gesture.
    :param points_Y: A list of Y-axis values of a gesture.

    :return:
        sample_points_X: A list of X-axis values of a gesture after sampling, containing 100 elements.
        sample_points_Y: A list of Y-axis values of a gesture after sampling, containing 100 elements.
    '''
    sample_points_X, sample_points_Y = [], []
    # TODO: Start sampling (12 points)

    assert(len(points_X) == len(points_Y))
    assert(len(points_X) >= 2)

    # get path length; avoid divide by zero errors
    path_length = max(0.0000001, find_path_length(points_X, points_Y))

    # n points are connected by n - 1 segments
    total_segments = 99
    # now get points for each pair of point; every pair would get the number of points proportional to its length against total distance
    length = len(points_X)

    for index in range(length - 1):
        current_X = points_X[index]
        current_Y = points_Y[index]
        next_X = points_Y[index + 1]
        next_Y = points_Y[index + 1]
        
        pairwise_distance = calculate_distance(current_X, current_Y, next_X, next_Y)
        ratio = pairwise_distance / path_length
        # rethink about this; this could yield more points than required
        points_in_current_segment = math.ceil(total_segments*ratio)
        sampled_X, sampled_Y = get_equidistant_points(current_X, current_Y, next_X, next_Y, points_in_current_segment)
        sample_points_X.extend(sampled_X)
        sample_points_Y.extend(sampled_Y)

    return sample_points_X, sample_points_Y


# Pre-sample every template
template_sample_points_X, template_sample_points_Y = [], []
for i in range(10000):
    X, Y = generate_sample_points(template_points_X[i], template_points_Y[i])
    template_sample_points_X.append(X)
    template_sample_points_Y.append(Y)


def do_pruning(gesture_points_X, gesture_points_Y, template_sample_points_X, template_sample_points_Y):
    '''Do pruning on the dictionary of 10000 words.

    In this function, we use the pruning method described in the paper (or any other method you consider it reasonable)
    to narrow down the number of valid words so that the ambiguity can be avoided to some extent.

    :param gesture_points_X: A list of X-axis values of input gesture points, which has 100 values since we have
        sampled 100 points.
    :param gesture_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we have
        sampled 100 points.
    :param template_sample_points_X: 2D list, containing X-axis values of every template (10000 templates in total).
        Each of the elements is a 1D list and has the length of 100.
    :param template_sample_points_Y: 2D list, containing Y-axis values of every template (10000 templates in total).
        Each of the elements is a 1D list and has the length of 100.

    :return:
        valid_words: A list of valid words after pruning.
        valid_probabilities: The corresponding probabilities of valid_words.
        valid_template_sample_points_X: 2D list, the corresponding X-axis values of valid_words. Each of the elements
            is a 1D list and has the length of 100.
        valid_template_sample_points_Y: 2D list, the corresponding Y-axis values of valid_words. Each of the elements
            is a 1D list and has the length of 100.
    '''
    valid_words, valid_template_sample_points_X, valid_template_sample_points_Y = [], [], []
    # TODO: Set your own pruning threshold
    threshold = 20
    # TODO: Do pruning (12 points)

    gestures_length_X = len(gesture_points_X) 
    gestures_length_Y = len(gesture_points_Y) 
    templates_length_X = len(template_points_X)
    templates_length_Y = len(template_points_Y)

    assert(gestures_length_X == gestures_length_Y)
    assert(templates_length_X == template_points_Y)
    assert(gestures_length_X == templates_length_X)

    first_gesture_X, first_gesture_Y = gesture_points_X[0], gesture_points_Y[0]
    last_gesture_X, last_gesture_Y = gesture_points_X[99], gesture_points_Y[99]

    for index in range(templates_length_X):
        curr_template_X, curr_template_Y  = template_sample_points_X[index], template_sample_points_Y[index]
        start_x, start_y = curr_template_X[0], curr_template_Y[0] 
        end_x, end_y = curr_template_X[99], curr_template_Y[99] 
        start_distance = calculate_distance(start_x, start_y, first_gesture_X, first_gesture_Y)
        end_distance = calculate_distance(end_x, end_y, last_gesture_X, last_gesture_Y)

        if start_distance <= threshold and end_distance <= threshold:
           valid_template_sample_points_X.append(curr_template_X)
           valid_template_sample_points_Y.append(curr_template_Y)
           valid_words.append(words[index])


    return valid_words, valid_template_sample_points_X, valid_template_sample_points_Y

# 
def compute_pairwise_distance(template_X, template_Y, gesture_sample_points_X, gesture_sample_points_Y):
        
        distance = 0
        
        for sample_index in range(sample_length):
            template_X = current_template_X[sample_index]
            template_Y = curr_template_Y[sample_index]
            gesture_X = gesture_sample_points_X[sample_index]
            gesture_Y = gesture_sample_points_Y[sample_index]

            distance += calculate_distance(template_X, template_Y, gesture_X, gesture_Y)

        return distance

def get_shape_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y):
    '''Get the shape score for every valid word after pruning.

    In this function, we should compare the sampled input gesture (containing 100 points) with every single valid
    template (containing 100 points) and give each of them a shape score.

    :param gesture_sample_points_X: A list of X-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param gesture_sample_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param valid_template_sample_points_X: 2D list, containing X-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.
    :param valid_template_sample_points_Y: 2D list, containing Y-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.

    :return:
        A list of shape scores.
    '''
    shape_scores = []
    # TODO: Set your own L
    L = 1

    # TODO: Calculate shape scores (12 points)

    assert(len(gesture_sample_points_X) == len(gesture_sample_points_Y))
    assert(len(valid_template_sample_points_X) == len(valid_template_sample_points_Y))
    assert(len(gesture_sample_points_X) == len(valid_template_sample_points_X))

    candidate_length = len(gesture_sample_points_X)
    sample_length = 100
    
    for index in range(candidate_length):
        current_template_X = valid_template_sample_points_X[index] 
        current_template_Y = valid_template_sample_points_Y[index]
        pairwise_distance = compute_pairwise_distance(template_X, template_Y, gesture_sample_points_X, gesture_sample_points_Y)
        shape_scores.append(pairwise_distance // sample_length)

    return shape_scores


def get_location_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y):
    '''Get the location score for every valid word after pruning.

    In this function, we should compare the sampled user gesture (containing 100 points) with every single valid
    template (containing 100 points) and give each of them a location score.

    :param gesture_sample_points_X: A list of X-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param gesture_sample_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param template_sample_points_X: 2D list, containing X-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.
    :param template_sample_points_Y: 2D list, containing Y-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.

    :return:
        A list of location scores.
    '''
    location_scores = []
    radius = 15
    # TODO: Calculate location scores (12 points)

    assert(len(gesture_sample_points_X) == len(gesture_sample_points_Y))
    assert(len(valid_template_sample_points_X) == len(valid_template_sample_points_Y))
    assert(len(gesture_sample_points_X) == len(valid_template_sample_points_X))

    candidate_length = len(gesture_sample_points_X)
    sample_length = 100
    
    for index in range(candidate_length):
        current_template_X = valid_template_sample_points_X[index] 
        current_template_Y = valid_template_sample_points_Y[index]

        distance = 0

        for i in range(sample_length):
            X, Y = current_template_X[i], curr_template_Y[i] 
            min_distance = float("inf")
            
            for j in range(sample_length):
                template_X = current_template_X[sample_index]
                template_Y = curr_template_Y[sample_index]
                distance = calculate_distance(X, Y, template_X, template_Y)
                min_distance = min(min_distance, distance) 

            gamma_i = max(min_distance - radius, 0)
            
            if gamma_i != 0:
                # using distance as a flag, I know its ugly!
                distance = 1
                break

        # now compute the pairwise distance between templates
        if distance != 0:
            distance = compute_pairwise_distance(template_X, template_Y, gesture_sample_points_X, gesture_sample_points_Y)

        location_scores.append(distance)

    return location_scores

def get_integration_scores(shape_scores, location_scores):
    integration_scores = []
    # TODO: Set your own shape weight
    shape_coef = 0.5
    # TODO: Set your own location weight
    location_coef = 1.0
    for i in range(len(shape_scores)):
        integration_scores.append(shape_coef * shape_scores[i] + location_coef * location_scores[i])
    return integration_scores


def get_best_word(valid_words, integration_scores):
    '''Get the best word.

    In this function, you should select top-n words with the highest integration scores and then use their corresponding
    probability (stored in variable "probabilities") as weight. The word with the highest weighted integration score is
    exactly the word we want.

    :param valid_words: A list of valid words.
    :param integration_scores: A list of corresponding integration scores of valid_words.
    :return: The most probable word suggested to the user.
    '''
    best_word = 'the'
    # TODO: Set your own range.
    n = 5
    # TODO: Get the best word (12 points)
    integration_scores.sort()

    return " ".join(best_word[:n])


@app.route("/")
def init():
    return render_template('index.html')


@app.route('/shark2', methods=['POST'])
def shark2():

    start_time = time.time()
    data = json.loads(request.get_data())

    gesture_points_X = []
    gesture_points_Y = []
    for i in range(len(data)):
        gesture_points_X.append(data[i]['x'])
        gesture_points_Y.append(data[i]['y'])
    gesture_points_X = [gesture_points_X]
    gesture_points_Y = [gesture_points_Y]

    gesture_sample_points_X, gesture_sample_points_Y = generate_sample_points(gesture_points_X, gesture_points_Y)

    # valid_words, valid_template_sample_points_X, valid_template_sample_points_Y = do_pruning(gesture_points_X, gesture_points_Y, template_sample_points_X, template_sample_points_Y)

    # print(valid_words)

    # shape_scores = get_shape_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y)

    # location_scores = get_location_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y)

    # integration_scores = get_integration_scores(shape_scores, location_scores)

    # best_word = get_best_word(valid_words, integration_scores)

    # end_time = time.time()
    return json.dumps({})
    # return '{"best_word":"' + best_word + '", "elapsed_time":"' + str(round((end_time - start_time) * 1000, 5)) + 'ms"}'


if __name__ == "__main__":
    app.run()
