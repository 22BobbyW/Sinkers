import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
import sys
from numpy.core.numeric import ones
from time import sleep

def sensor_position(pix_x, pix_y, res_x, res_y):
    sensor_width,sensor_height = (0.00368, 0.00276) #mm to meters
    origin = (res_x/2,res_y/2)
    ratio_x, ratio_y = (sensor_width/res_x, sensor_height/res_y)
    
    pix_x, pix_y = (pix_x - origin[0], pix_y - origin[1])

    sensor_pos_x, sensor_pos_y = (ratio_x*pix_x, ratio_y*pix_y)
    
    return (sensor_pos_x, sensor_pos_y)


focal_length = 0.00304 #mm is the focal length

def sensor_angle(sensor_pos_x, sensor_pos_y, f):
    return np.degrees(np.arctan2(sensor_pos_x,f))


def find_centers(filter_image, rgb_image, thresh):
    object_detection_surface = cv2.boxFilter(filter_image.astype(int), -1, (20, 20), normalize=False)

    if np.max(object_detection_surface) <= 0:
        return [], []

    object_detection_surface = object_detection_surface * 255/np.max(object_detection_surface)
    # threshold = thresh * 255 / np.max(object_detection_surface)

    img8 = object_detection_surface.astype(np.uint8)

    threshold, img_out = cv2.threshold(img8, thresh, 255, cv2.THRESH_BINARY)

    if cv2.__version__ == '3.2.0':
        _, contours, hierarchy = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        contours, hierarchy = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    centers = []
    angles = []
    for contour in contours:
        np.max([item[0][0] for item in contour])

        point = np.mean(contour, axis = 0)[0,:]
        centers.append(point)
        
        a = sensor_position(point[0], point[1], rgb_image.shape[1], rgb_image.shape[0])
        b = sensor_angle(a[0], a[1], focal_length)
        
        angles.append(b)
    return centers, angles

def get_ranges(red_range, green_range, blue_range, rgb_image):
    rgb_filt = cv2.boxFilter(rgb_image, -1, (5,5))

    red_filt = rgb_filt[:,:,0]
    green_filt = rgb_filt[:,:,1]
    blue_filt = rgb_filt[:,:,2]

    img_thresh_red = np.logical_and(red_filt > red_range[0], red_filt < red_range[1])
    img_thresh_green = np.logical_and(green_filt > green_range[0], green_filt < green_range[1])
    img_thresh_blue = np.logical_and(blue_filt > blue_range[0], blue_filt < blue_range[1])

    img_thresh_RG = np.logical_and(img_thresh_red, img_thresh_green)
    img_thresh_RGB = np.logical_and(img_thresh_RG, img_thresh_blue)

    return(img_thresh_RGB)

def detect_buoys(img):
    # hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_image = np.flip(img, axis=2) 
    # rgb_image = np.flip(rgb_image, 0)

    r_red_range = (40,100)
    r_green_range = (75,120)
    r_blue_range = (180,240)

    g_red_range = (7,50)
    g_green_range = (150,255)
    g_blue_range = (180,255)

    img_thresh_red = get_ranges(r_red_range, r_green_range, r_blue_range, rgb_image)
    img_thresh_green = get_ranges(g_red_range, g_green_range, g_blue_range, rgb_image)

    reds_centers, reds_angles = find_centers(img_thresh_red, rgb_image, 50)
    greens_centers, green_angles = find_centers(img_thresh_green, rgb_image, 15)
    return green_angles, reds_angles # , greens_centers, reds_centers

'''fig, ax = plt.subplots()
for frame_num in range(1, 4):

    img = cv2.imread(f'real/frame_{frame_num}.jpg') 
    
    g_angles, r_angles, g_centers, r_centers = detect_buoys(img)

    img = np.flip(img, axis=2)
    # print(frame_num)
    print('\n')
    print(g_angles)
    print(r_angles)
    ax.clear()
    ax.imshow(img)
    print(g_centers)
    print(r_centers)
    if len(g_centers) != 0:
        ax.plot(g_centers[0][0], g_centers[0][1], 'bo')
    if len(r_centers) != 0:
        ax.plot(r_centers[0][0], r_centers[0][1], 'ro')
    plt.pause(1)
    plt.draw()'''
