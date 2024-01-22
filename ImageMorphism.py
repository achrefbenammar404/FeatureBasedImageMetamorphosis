import cv2
import numpy as np
import math
import sys
from argparse import ArgumentParser
import time
from Line import Line 



class ImageMorpher : 
    
    
    @staticmethod
    def get_feature_line(event, x, y, flags, param):
        img = param[0]
        point_list = param[1]
        line_list = param[2]
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 2, (0, 0, 255), thickness=-3)
            point_list.append(np.array([y, x]))   # store current point

            if len(param[1]) % 2 == 0:  # if 2 points, make a line
                cv2.line(img, (point_list[-2][1], point_list[-2][0]), (x, y), (0, 0, 255), 2)
                line = Line(np.array(point_list[-2]), np.array([y, x]))   # create a line object and store it
                line_list.append(line)
                
                

   

    # map the P in destination image to source image
    @staticmethod
    def mapping(cur_point, src_vector, inter_vector, p=0, a=1, b=2):
        src_perpen = src_vector.perpendicular # perpendicular vector
        PQ_perpen = inter_vector.perpendicular
        inter_start_point = inter_vector.start_point

        PX = cur_point - inter_start_point  # PX vector
        PQ = inter_vector.vector      # PQ vector, destination vector

        inter_len = inter_vector.length   # len of destination vector

        u = np.inner(PX, PQ) / inter_len    # calculate u and v
        v = np.inner(PX, PQ_perpen) / inter_vector.sqrt_len
        
        PQt = src_vector.vector       # PQ vector in src img
        src_len = src_vector.sqrt_len  # its length
        xt = src_vector.start_point + u * PQt + v * src_perpen / src_len    # Xt point

        # calculate the distance from Xt to PQ vector in src img depend on u
        dist = 0
        if u < 0:
            dist = np.sqrt(np.sum(np.square(xt - src_vector.start_point)))
        elif u > 1: 
            dist = np.sqrt(np.sum(np.square(xt - src_vector.end_point)))
        else:
            dist = abs(v)
        
        # calculate weight of this point
        weight = 0
        length = pow(inter_vector.sqrt_len, p)
        weight = pow((length / (a + dist)), b)

        return xt, weight

    # do bilinear of given point and img on its color
    @staticmethod
    def bilinear(img, point, h, w):
        x, y = point[0], point[1]
        x1, x2 = math.floor(x), math.ceil(x)    # ceiling and floor point
        y1, y2 = math.floor(y), math.ceil(y)
        if x2 >= h:                             # limit the range
            x2 = h - 1
        if y2 >= w:
            y2 = w - 1
        a, b = x - x1, y - y1
        # bilinear, get the color array (3,)
        val = (1 - a) * (1 - b) * img[x1, y1] + a * (1 - b) * img[x2, y1] + (1 - a) * b * img[x1, y2] + a * b *img[x2, y2]
        
        return val

    # warping image
    @staticmethod
    def warpImg(img , src_vectors, inter_vectors, p=0, a=1, b=2):
        h, w, _ = img.shape
        warp_img = np.empty_like(img)   # result img

        # loop every pixel
        
        i =0 
        while i < h :
            j = 0 
            while j < w :
                psum = np.array([0, 0])
                wsum = 0
                # calculate the mapping point on src img of this point
                l = len(inter_vectors)
                idx = 0 
                while idx < l :
                    xt, weight = ImageMorpher.mapping(np.array([i, j]), src_vectors[idx], inter_vectors[idx], p, a, b)
                    psum = psum + xt * weight   # weighted point amd sum up
                    wsum = wsum + weight # weight sum up
                    idx +=1
                point = psum / wsum             # final point

                if point[0] < 0:                # limit the range
                    point[0] = 0
                elif point[0] >= h:
                    point[0] = h - 1
                if point[1] < 0:
                    point[1] = 0
                elif point[1] >= w:
                    point[1] = w - 1
                
                warp_img[i, j] = ImageMorpher.bilinear(img, point, h, w) # calulate the color by bilinear
                j+=1
            i+=1
        return warp_img   
    
    @staticmethod
    def morph_on_features(src_origin , line_coordinates_src , line_coordinates_dst , a  , b   , p   ):
        """morph src image to dst image based on lines defined by their coordinates 

        Args:
            src_origin (_ArrayLike_): _Source image in array form_
            line_coordinates_src (_list_): _list each element is a numpy array  = (y , x)_
            line_coordinates_dst (_list_): _list each element is a numpy array = (y , x)_
        """
        src_lines = Line.get_lines_from_points(line_coordinates_src)
        dst_lines = Line.get_lines_from_points(line_coordinates_dst)
        src_warp = ImageMorpher.warpImg(src_origin , src_lines , dst_lines, p , a , b  )
        return src_warp