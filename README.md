# SHARK^2 #
Implementation of Shark2 Algorithm

There are five steps:
- Sampling
- Pruning
- Shape Score
- Location Score
- Compute Integration score and return top-n words


### Sampling ###
The user template and the word templates can be simply viewed as vectors. In order to meaninfully compare two vectors they have be of equal size. We have chosen 100 to be the size of our vectors. So we need to sample 100 equidistant points in the user template and the model template. The approach is the following:
- Compute the path length template length by calculating pairwise points length on the template.
- In order to get 100 equidistant points I choose number of points on each segment in proportion to how much it would contribute to the overall path length.
- We apply the same algorithm for sampling equidistant points for both user and word template.
- While in practice this algorithm doesn't guarantee perfectly equidistant points it's quite effective and efficient.

### Pruning ###
- In order to reduce the number of potential candidates for matching, we retain only those words which lie close match to the starting and end character of the user template.
- The threshold is set at 15 units.

### Shape Score ###
- Summation of average euclidean distance between the points in the user template and the word template.

### Location Score ###
- Implemented as given in the paper.

### Return Top N Words ###
- Have set the weights as 0.9 for shape score and 0.1 for location score. Imposing more penalty for deviations in shape score.
- Sort the list by integration scores and return the lowest one. Since it is very unlikely that the scores are going to overlap returning the words which lie in vicinity to the closest match too. The threshold was set at 5.

