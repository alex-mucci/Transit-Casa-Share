GIS Processes by Data Field


Census block Level Data

- Spatial Join (intersect)
	- sum all of the data fields
	- sum the area of the census block data
	- issue of double counting census block data

Census Tract Level Data

- Spatial Join (intersect)
	- join the census tract data to bus stop point features 
		- multiple stops will be assigned the same data

Competiting Transit Data

- Spatial Join (intersect)
	-any station locations that are within a buffer ridership, for that station is added to that buffer

** Eventually need to run intersections of each of the data files and the buffers. Then calculate areas of the smaller intersected polygons and scale the original data by the interseted area/original area. 
Ex. half of a census block's area is overlapping with a buffer, then half of the original employment/population/ect. is assigned to the new polygon created within the buffer by the intersection.

Lastly a spatial join (intersect) is ran to add the intersected polygons that are within the buffers to the buffers, making sure to sum all of the data fields of interest. 
*** Scaling the data by area within a buffer has been accomplished as of 6/15/17

