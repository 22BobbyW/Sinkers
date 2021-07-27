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


def find_angles(center):
    angles = []
    result = get_angles(sensor_position(center[1], center[0]))
    if result is not None:
        angles.append(result)
    return angles

def detect_buoys(img):
    if img is None:
        return [],[]
    
    img = np.flip(img, axis=2) 
    g_angles = []
    r_angles = []
    g_center = []
    r_center = []
    img = cv2.boxFilter(img, -1, (5, 5))
    
    rfilt = img[:, :, 0]
    gfilt = img[:, :, 1]
    bfilt = img[:, :, 2]

    img_thresh_red_g = np.logical_and(rfilt > 15, rfilt < 40)
    img_thresh_green_g = np.logical_and(gfilt > 105, gfilt < 225)
    img_thresh_blue_g = np.logical_and(bfilt > 170, bfilt < 210)



    img = cv2.boxFilter(img, -1, (10, 10))
    rfilt = img[:, :, 0]
    gfilt = img[:, :, 1]
    bfilt = img[:, :, 2]
    img_thresh_green_r = np.logical_and(gfilt > 75, gfilt < 120)
    img_thresh_red_r = np.logical_and(rfilt > 40, rfilt < 100)
    img_thresh_blue_r = np.logical_and(bfilt > 170, bfilt < 210)

    img_thresh_r = np.logical_and(img_thresh_red_r, img_thresh_green_r, img_thresh_blue_r)
    img_thresh_g = np.logical_and(img_thresh_red_g, img_thresh_blue_g, img_thresh_green_g)
    
    obs_g = cv2.boxFilter(img_thresh_g.astype(int), -1, (50,50), normalize=False)
    obs_r = cv2.boxFilter(img_thresh_r.astype(int), -1, (50,50), normalize=False)

    # img8_g = (obs_g * 255 / np.max(img)).astype(np.uint8)
    # thresh8_g = (50 * 255 / np.max(img)).astype(np.uint8)

    # img8_r = (obs_r * 255 / np.max(img)).astype(np.uint8)
    # thresh8_r = (80 * 255 / np.max(img)).astype(np.uint8)

    g = np.argwhere(obs_g>50)
    r = np.argwhere(obs_r>80)

    if g.size != 0:
        g_center = np.average(g, axis=0)
        g_angles = find_angles(g_center)
    if r.size != 0:
        r_center = np.average(r, axis=0)
        r_angles = find_angles(r_center)

    return g_angles, r_angles

'''fig, ax = plt.subplots()
for frame_num in range(1627424218, 1627424229):
    if frame_num == 1627422410:
        continue
    # if frame_num == 1627422424:
    #     continue
    img = cv2.imread(f'frames/frame_{frame_num}.jpg')
    # img = np.flip(img, axis=2) 
    g_centers, r_centers, g_angle, r_angle = detect_buoys(img)
    # print(frame_num)
    print('\n')
    print(g_angle)
    print(r_angle)
    ax.clear()
    ax.imshow(img)
    if len(g_centers) != 0:
        ax.plot(g_centers[1], g_centers[0], 'bo')
    if len(r_centers) != 0:
        ax.plot(r_centers[1], r_centers[0], 'ro')
    plt.pause(1)
    plt.draw()'''