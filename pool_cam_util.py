import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

def sensor_position(pix_x, pix_y, res_x=640, res_y=480): 
    x = 3.68 
    y = 2.76 
    sensor_pos_x = (pix_x - (res_x / 2.0)) / res_x * 3.68
    sensor_pos_y = (pix_y - (res_y / 2.0)) / res_x * 2.76
    return (sensor_pos_x, sensor_pos_y) 


def get_angles(sensor_pos):
    sensor_pos_x, sensor_pos_y = sensor_pos
    f = 3.04 
    horizontal_angle = np.arctan2(sensor_pos_x, f) 
    horizontal_angle = np.degrees(horizontal_angle)
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

    sorted_c = sorted(contours, key=cv2.contourArea, reverse= True)


    centers = []    
    angles = []
    
    contour = sorted_c[0]
    print(cv2.contourArea(contour))
    center = np.mean(contour, axis = 0)[0,:]
    sensor_pos = sensor_position(center[0], center[1])
    centers.append(center)
    angle = get_angles(sensor_pos)
    angles.append(angle)

    return centers, angles

def detect_buoys(img):
    g_angles = []
    r_angles = []
    g_center = []
    r_center = []
    img = np.flip(img, axis=2) 
    img = np.flip(img, 0)
    img = cv2.boxFilter(img, -1, (5, 5))

    
    rfilt = img[:, :, 0]
    gfilt = img[:, :, 1]
    bfilt = img[:, :, 2]

    img_thresh_red_g = np.logical_and(rfilt > 8, rfilt < 45)
    img_thresh_green_g = np.logical_and(gfilt > 120, gfilt < 210)
    img_thresh_blue_g = np.logical_and(bfilt > 200, bfilt < 225)

    img_thresh_red_r = np.logical_and(rfilt > 60, rfilt < 90)
    img_thresh_green_r = np.logical_and(gfilt > 80, gfilt < 110)
    img_thresh_blue_r = np.logical_and(bfilt > 200, bfilt < 225)

    img_thresh_RG_r = np.logical_and(img_thresh_red_r, img_thresh_green_r)
    img_thresh_r = np.logical_and(img_thresh_RG_r, img_thresh_blue_r)
    img_thresh_RG_g = np.logical_and(img_thresh_red_g, img_thresh_green_g)
    img_thresh_g = np.logical_and(img_thresh_RG_g, img_thresh_blue_g)
    
    obs_g = cv2.boxFilter(img_thresh_g.astype(int), -1, (10,10), normalize=False)
    obs_r = cv2.boxFilter(img_thresh_r.astype(int), -1, (10,10), normalize=False)

    r_centers, r_angles = contouring(obs_r, 50)
    g_centers, g_angles = contouring(obs_g, 50)

    plt.clf()
    plt.imshow(img)
    for center in r_centers:
        plt.plot(center[0], center[1], 'ro')
    for center in g_centers:
        plt.plot(center[0], center[1], 'bo')
    plt.show()
    plt.pause(1)
    plt.draw()

    # return g_angles, r_angles

    return g_center, r_center, g_angles, r_angles

for frame_num in range(1627586415, 1627586439):
    if frame_num == 1627586426:
        continue
    img = cv2.imread(f'frames/frame_{frame_num}.jpg')
    # img = np.flip(img, axis=2) 
    g_centers, r_centers, g_angle, r_angle = detect_buoys(img)
    # print(frame_num)
    print(g_angle)
    print(r_angle)
    print('\n')

