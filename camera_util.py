import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

def sensor_position(pix_x, pix_y, res_x=640, res_y=480): 
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
    if not math.isnan(horizontal_angle):
        return round(horizontal_angle)
    return None

def find_angles(center):
    angles = []
    result = get_angles(sensor_position(center[1], center[0]))
    if result is not None:
        angles.append(result)
    return angles


def detect_buoys(img):
    if img is None:
        return [], []
    img = cv2.boxFilter(img, -1, (10, 10))
    rfilt = img[:, :, 0]
    img_thresh_green = np.logical_and(rfilt > 0, rfilt < 160)
    gfilt = img[:, :, 1]
    img_thresh_red = np.logical_and(gfilt > 0, gfilt < 190)

    obs_g = cv2.boxFilter(img_thresh_green.astype(int), -1, (50,50), normalize=False)
    obs_r = cv2.boxFilter(img_thresh_red.astype(int), -1, (50,50), normalize=False)

    thresh = 0

    g_center = np.average((np.argwhere(obs_g>thresh)), axis=0)
    r_center = np.average((np.argwhere(obs_r>thresh)), axis=0)

    g_angles = find_angles(g_center)
    r_angles = find_angles(r_center)
    return g_angles, r_angles

img = cv2.imread("frames/frame_1627278988.jpg")
g,r = detect_buoys(img)
print(r)
print(g)