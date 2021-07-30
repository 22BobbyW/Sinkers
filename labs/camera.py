
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
import sys
from numpy.core.numeric import ones
from time import sleep
"""
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture('foo.jpg')
"""

def sensor_position(pix_x, pix_y, res_x, res_y):
    """
    a function that converts from pixel position to measurement units (meters)
    on the camera imaging sensor.
    """
    shifted_origin = True #for debugging
    sensor_width,sensor_height = (0.00368, 0.00276) #mm to meters
    origin = (res_x/2,res_y/2)
    ratio_x, ratio_y = (sensor_width/res_x, sensor_height/res_y)
    
    if shifted_origin == True:
        pix_x, pix_y = (pix_x - origin[0], pix_y - origin[1])

    sensor_pos_x, sensor_pos_y = (ratio_x*pix_x, ratio_y*pix_y)
    
    return (sensor_pos_x, sensor_pos_y)


focal_length = 0.00304 #mm is the focal length

def sensor_angle(sensor_pos_x, sensor_pos_y, f):
    """
    a helper function that gets the sensor angles
    """
    return((np.degrees(np.arctan2(sensor_pos_x,f)), np.degrees(np.arctan2(sensor_pos_y,f))))


def find_centers(filter_image, rgb_image):
    """
    a function that finds the centers and angles
    """
    object_detection_surface = cv2.boxFilter(filter_image.astype(int), -1, (50,50), normalize=False)
    
    thresh = 1000 #Between 0 and 2500 px
    object_detection_surface = object_detection_surface * 255/np.max(object_detection_surface)
    threshold = thresh * 255/ np.max(object_detection_surface)

    img8 = object_detection_surface.astype(np.uint8)

    # thresh, img_out = cv2.threshold(img8, threshold, 255, cv2.THRESH_BINARY)
    thresh, img_out = cv2.threshold(img8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, cv2.THRESH_BINARY)

    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) ###error
    contours, hierarchy = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    
    # plt.imshow(img_out)
    # print(contours)
    # contours = np.argwhere(contours>thresh)
    # print(object_detection_surface)
    centers = []
    angles = []
    for contour in contours:
        np.max([item[0][0] for item in contour])
        # print(contour,"\n--\n")


        center = np.mean(contour, axis = 0)[0,:]
        print(center)

        avg_x, avg_y = center
        print((avg_x, avg_y))
        
        centers.append(center)

        sensor_pos = sensor_position(center[0], center[1], rgb_image.shape[1], rgb_image.shape[0])
        print((np.round(sensor_pos[0]*1000,2), np.round(sensor_pos[1]*1000,2)),"mm", f"for the blue colored point.")
        
        angle = sensor_angle(sensor_pos[0], sensor_pos[1], focal_length)
        print(angle, "degrees")
        angles.append(angle)
    
    return centers, angles


def get_ranges(red_range, green_range, blue_range, hsv_image, rgb_image):
    plotting = True

    hue_img = hsv_image[:,:, 0]
    saturation_img = hsv_image[:,:, 1]
    value_img = hsv_image[:,:,2]

    red_img = rgb_image[:,:,0]
    green_img = rgb_image[:,:,1]
    blue_img = rgb_image[:,:,2]

    hsv_filt = cv2.boxFilter(hsv_image, -1, (10,10))
    # hue_filt = cv2.boxFilter(hue_img, cv2.CV_32F,(100,100))
    # saturation_filt = cv2.boxFilter(saturation_img, cv2.CV_32F,(100,100))
    # value_filt = cv2.boxFilter(value_img, cv2.CV_32F,(100,100))

    hue_filt = hsv_filt[:,:,0]
    saturation_filt = hsv_filt[:,:,1]
    value_filt = hsv_filt[:,:,2]

    rgb_filt = cv2.boxFilter(rgb_image, -1, (10,10))
    # red_filt = cv2.boxFilter(red_img, cv2.CV_32F,(100,100))
    # green_filt = cv2.boxFilter(green_img, cv2.CV_32F,(100,100))
    # blue_filt = cv2.boxFilter(blue_img, cv2.CV_32F,(100,100))

    red_filt = rgb_filt[:,:,0]
    green_filt = rgb_filt[:,:,1]
    blue_filt = rgb_filt[:,:,2]

    hue_range = (40,75)
    saturation_range = (90,190)
    value_range = (50,100)

    img_thresh_hue = np.logical_and(hue_filt > hue_range[0], hue_filt < hue_range[1])
    img_thresh_saturation = np.logical_and(saturation_filt > saturation_range[0], saturation_filt < saturation_range[1])
    img_thresh_value = np.logical_and(value_filt > value_range[0], value_filt < value_range[1])

    img_thresh_HS = np.logical_and(img_thresh_hue, img_thresh_saturation)
    img_thresh_HSV = np.logical_and(img_thresh_HS, img_thresh_value)

    img_thresh_red = np.logical_and(red_filt > red_range[0], red_filt < red_range[1])
    img_thresh_green = np.logical_and(green_filt > green_range[0], green_filt < green_range[1])
    img_thresh_blue = np.logical_and(blue_filt > blue_range[0], blue_filt < blue_range[1])

    img_thresh_RG = np.logical_and(img_thresh_red, img_thresh_green)
    img_thresh_RB = np.logical_and(img_thresh_red, img_thresh_blue)
    img_thresh_GB = np.logical_and(img_thresh_green, img_thresh_blue)
    img_thresh_RGB = np.logical_and(img_thresh_RG, img_thresh_blue)
    
    if (plotting):
    
        if False:
            plt.title("rgb filt")
            plt.imshow(rgb_filt)
            plt.show()

        if False:
            rows, columns = (2,3)
            fig, ax = plt.subplots(rows,columns, figsize=(15,10))

            #plotting
            ax[0][1].set_title("rgb")
            ax[0][0].imshow(red_filt, cmap = "Reds")
            ax[0][1].imshow(green_filt, cmap="Greens")
            ax[0][2].imshow(blue_filt, cmap="Blues")
            ax[1][1].set_title("hsv")
            ax[1][0].imshow(hue_filt)
            ax[1][1].imshow(saturation_filt)
            ax[1][2].imshow(value_filt)

            #plot the colorbar
            fig.colorbar(cm.ScalarMappable(), ax=ax)
            plt.show()

        if (False): 
            rows, columns = (2,3)
            fig, ax = plt.subplots(rows,columns, figsize=(15,10))

            ax[0][0].imshow(img_thresh_red)
            ax[0][1].imshow(img_thresh_green)
            ax[0][2].imshow(img_thresh_blue)

            ax[1][0].imshow(img_thresh_red)
            ax[1][1].imshow(img_thresh_RG)
            ax[1][2].imshow(img_thresh_RGB)
            #plot the colorbar
            fig.colorbar(cm.ScalarMappable(), ax=ax)
            plt.show()

        
        if False:
            rows, columns = (2,3)
            fig, ax = plt.subplots(rows,columns, figsize=(15,10))

            ax[0][0].imshow(img_thresh_hue)
            ax[0][1].imshow(img_thresh_saturation)
            ax[0][2].imshow(img_thresh_value)

            ax[1][0].imshow(img_thresh_hue)
            ax[1][1].imshow(img_thresh_HS)
            ax[1][2].imshow(img_thresh_HSV)
            #plot the colorbar
            fig.colorbar(cm.ScalarMappable(), ax=ax)
            plt.show()

    
    return(img_thresh_RGB)

def detect_buoys(img):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    r_red_range = (65,100) #61,106,205
    r_green_range = (75,120)
    r_blue_range = (170,210)

    g_red_range = (25,40)
    g_green_range = (115,225)
    g_blue_range = (180,210)

    img_thresh_red = get_ranges(r_red_range, r_green_range, r_blue_range, hsv_image, rgb_image)
    img_thresh_green = get_ranges(g_red_range, g_green_range, g_blue_range, hsv_image, rgb_image)

    reds_centers, reds_angles = find_centers(img_thresh_red, rgb_image)
    greens_centers, green_angles = find_centers(img_thresh_green, rgb_image)
    
    plt.clf()
    plt.imshow(rgb_image)
    for center in reds_centers:
        plt.plot(center[0], center[1], 'ro')

    for center in greens_centers:
        plt.plot(center[0], center[1], 'go')
    # plt.show()
    plt.pause(1)
    plt.draw()
    
    

    return greens_centers, reds_centers, green_angles, reds_angles

file_name = []
images = []
centers = []
begin, end = (1627339222, 1627339237)
i = 0
for framenumber in range(begin, end+1):
    if(framenumber != 1627339229):
        
        # print(framenumber)
        # print(i)
        file_name.append(f"frames/frame_{framenumber:10d}.jpg")
        print(file_name[i])
        images.append(cv2.imread(file_name[i]))
        images[i] = cv2.resize(images[i], (640, 480))
        
        #print("updated resolution:", (img.shape[1], img.shape[0]), "pixels")        
        # image = np.flip(images[i], axis = 2)
        # plt.imshow(image)
        # plt.show()

        img = images[i]
        detect_buoys(img)
        i+=1