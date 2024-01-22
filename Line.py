import numpy as np 



# line structure, store its start point and end point
class Line(object):
    def __init__(self, start_point, end_point):
        self.start_point = start_point  # both points are stored as np.array
        self.end_point = end_point

        self.vector = self.end_point - self.start_point
        self.perpendicular = np.array([self.vector[1], -self.vector[0]])

        self.length = np.sum(np.square(self.vector))
        self.sqrt_len = np.sqrt(self.length)
    
    def print_content(self):    # for debugging
        print('start {} end {} vector {} perpen {}'.format(self.start_point, self.end_point, self.vector, self.perpendicular))
    
    @staticmethod
    def get_lines_from_points(coordinates) : 
        """takes in a list of coordinates for the points describing the feature lines 
        each coordinate is a numpy array 
        the corrdinates adjacent to each other will form a line 
        for example [y0 , x0] is the start point [x1 , y1] is the end point for the line 
        with x0 being the x coordinate of the kist at index 0 
        return a list of lines 
        Args:
            coordinates (_type_): _list of np.array s _

        Returns:
            _type_: _list of lines _
        """
        assert len(coordinates) % 2 == 0  
        return [Line(coordinates[i] , coordinates[i+1])  for i in range (0 , len(coordinates)-1 , 2)]