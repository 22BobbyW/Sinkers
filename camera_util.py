import numpy as np
import cv2
import matplotlib.pyplot as plt

def sensor_position(pix_x, pix_y, res_x=3280, res_y=2464): 
    x = 3.68 
    y = 2.76 
    sensor_pos_x_pixel = pix_x - res_x / 2
    sensor_pos_y_pixel = pix_y - res_y / 2
    sensor_pos_x = round(sensor_pos_x_pixel * x / res_x, 5)
    sensor_pos_y = round(sensor_pos_y_pixel * y / res_y, 5)
    return (sensor_pos_x, sensor_pos_y) 

def get_angles(sensor_pos):
    sensor_pos_x, sensor_pos_y = sensor_pos
    f = 3.04 
    horizontal_angle = np.arctan2(sensor_pos_x, f) * 180 / np.pi
    vertical_angle = np.arctan2(sensor_pos_y, f) * 180 / np.pi
    return (horizontal_angle)

def find_angles(center):
    angles = []
    angles.append(get_angles(sensor_position(center[1], center[0])))
    return angles


def detect_buoys(img):
    img = cv2.boxFilter(img, -1, (10, 10))
    rfilt = img[:, :, 0]
    img_thresh_green = np.logical_and(rfilt > 0, rfilt < 120)
    gfilt = img[:, :, 1]
    img_thresh_red = np.logical_and(gfilt > 0, gfilt < 150)

    obs_g = cv2.boxFilter(img_thresh_green.astype(int), -1, (50,50), normalize=False)
    obs_r = cv2.boxFilter(img_thresh_red.astype(int), -1, (50,50), normalize=False)

    thresh = 50

    g_center = np.average((np.argwhere(obs_g>thresh)), axis=0)
    r_center = np.average((np.argwhere(obs_r>thresh)), axis=0)

    g_angles = find_angles(g_center)
    r_angles = find_angles(r_center)
    return g_angles, r_angles