# shark2
Implementation of Shark2 Algorithm

There are five steps:
- Sampling
- Pruning
- Location Score
- Shape Score
- Compute Integration score and return top-n words


### Sampling ###

The user template and the word templates can be simply viewed as vectors. In order to meaninfully compare two vectors they have be of equal size. We have chosen 100 to be the size of our vectors. So we need to sample 100 equidistant points in the user template and the model template. The approach is the following:
- Compute the path length template length by calculating pairwise points length on the template.
- In order to get 100 equidistant points we choose number of points on each segment in proportion to how much it would contribute to the overall path length.
- We apply the same algorithm for sampling equidistant points for both user and word template.

### Pruning ###

- In order to reduce the number of potential candidates for matching, we retain only those words which lie close match to the starting and end character of the user template.  
