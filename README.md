This takes in contours in QGIS, 

Smoothes them, and figures out for each vertex what the average shift of the nearby vertices is

Then this average shift is applied to the vertices, before they are construced back into lines

The smoothing algorithm is set up as distance weighted McMaster, though it can be changed to other algorithms, as long as whatever algorithm is used doesn't change the number of vertices in each line
