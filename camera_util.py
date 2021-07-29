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
        return round(horizontal_angle, 2)
    return None

def contouring(obs, thresh):
    if np.max(obs) <= 0:
        return [], []
    obs = obs * 255/np.max(obs)
    img8 = obs.astype(np.uint8)
    thresh, img_out = cv2.threshold(img8, thresh, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    centers = []    
    angles = []
    for contour in contours:
        center = np.mean(contour, axis = 0)[0,:]
        centers.append(center)
        sensor_pos = sensor_position(center[0], center[1])
        angle = get_angles(sensor_pos)
        angles.append(angle)
    return centers, angles

def detect_buoys(img):
    if img is None:
        return [],[]
    
    img = np.flip(img, axis=2)

    g_angles = []
    r_angles = []
    g_center = []
    r_center = []
    img = cv2.boxFilter(img, -1, (6, 6))
    
    rfilt = img[:, :, 0]
    gfilt = img[:, :, 1]
    bfilt = img[:, :, 2]

    img_thresh_red_g = np.logical_and(rfilt > 12, rfilt < 40)
    img_thresh_green_g = np.logical_and(gfilt > 110, gfilt < 255)
    img_thresh_blue_g = np.logical_and(bfilt > 180, bfilt < 240)

    img_thresh_red_r = np.logical_and(rfilt > 40, rfilt < 100)
    img_thresh_green_r = np.logical_and(gfilt > 75, gfilt < 120)
    img_thresh_blue_r = np.logical_and(bfilt > 180, bfilt < 240)

    img_thresh_RG_r = np.logical_and(img_thresh_red_r, img_thresh_green_r)
    img_thresh_r = np.logical_and(img_thresh_RG_r, img_thresh_blue_r)
    img_thresh_RG_g = np.logical_and(img_thresh_red_g, img_thresh_green_g)
    img_thresh_g = np.logical_and(img_thresh_RG_g, img_thresh_blue_g)
    
    obs_g = cv2.boxFilter(img_thresh_g.astype(int), -1, (50,50), normalize=False)
    obs_r = cv2.boxFilter(img_thresh_r.astype(int), -1, (50,5), normalize=False)

    r_centers, r_angles = contouring(obs_r, 55)
    g_centers, g_angles = contouring(obs_g, 50)

    return g_angles, r_angles