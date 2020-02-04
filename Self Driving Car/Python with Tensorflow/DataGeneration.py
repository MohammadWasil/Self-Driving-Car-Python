import numpy as np
from PIL import ImageGrab
import cv2
import time
import os
import socket

filename = 'D:/ML/Unity-ML/sdcdata_1.csv'

firstTime = time.time()
booleanvalue = True

steeringAngle = []
velocity = []
throttle = []
'''
To be saved in csv file.
'''
input_image = []
local_address_image = []

masked_image_array = []

# Socket Tcp Connection.
host = "127.0.0.1"
port = 25001            # Port number
#data = "1,1,11"         # Data to be send
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # TCP connection
print("starting connection")
try:
    sock.connect((host, port))                  #To connet\ct ot the given port.
    print("Connected")
finally:
    print("Might happen socket is closed!")
#######

path = 'D:/ML/Unity-ML/SDC'         # Destination/path to which all the images will be saved
num = 0 

# a little help fromk github page.
def moving_Average(data, window):
    return [int(x) for x in np.average(data[-window:], axis = 0 )]          # moving average over a window of 10 previously identified lines to smooth out the lane lines.

def separate_lines(image, lines):
       
    left_lines = []
    right_lines = []
    left_lanes_history = []
    right_lanes_history = []
    m = 0
    try:
        for line in lines:
            for x1, y1, x2, y2 in line:
                                
                if (x1 == x2) or (y1 == y2):    # skips the lines where slope is equal to zero
                    continue
                
                m = ((y2 - y1) / ( x2 - x1))
                if( m > -0.5 and m < 0.5) or m < -1 or m > 1:  #skip horizontal lines.
                    continue
                
                if m < 0:               # it is a left lane
                    left_lines += [(x1, y1, x2, y2, m)]     # packing all the values in an array left_lines
                
                elif m > 0:             # it is a right lane
                    right_lines += [(x1, y1, x2, y2, m)]    # packing all the values in an array right_lines
            
        imshape = image.shape                               # to get the shape of the image i.e (300, 300, 3), the three channels.
        
        left_lane = [0, imshape[0], 0, (imshape[0]*0.611)]    # x1, y1, ,x2, y2 values in left_lane, now we have to find the vale of x1, and x2 in left lane.
        right_lane = [0, imshape[0], 0, (imshape[0]*0.611)]   # x1, y1, ,x2, y2 values in right_lane, now we have to find the vale of x1, and x2 in right lane.
        
        if len(left_lines):                                     # if there is something in the array
            
            left_lane_avg = np.mean(left_lines, axis = 0)       # taking the average of all the values of the line and storing in the array left_lane_avg
            
            # we have slope(m), y1 and y2. To calculate x1 and x2, first we'll calculate intercept.
            # y = mx + c, here c is the intercept.
            # Therefore,  c = y - mx
            # since, we have to find two values of x, therefore, their will be two values of c
            # c1 = y1 - m * x1
            left_c_x1 = left_lane_avg[1] - left_lane_avg[4] * left_lane_avg[0]      # To calclate c, we need all average values of y, m, x.
            left_c_x2 = left_lane_avg[3] - left_lane_avg[4] * left_lane_avg[2]
            
            # Now, we got our c values, we'll calculate x1, and x2, with their corresponding intercept.
            # x = (y - c) / m
            # Therefore, x1 = y1 - c / m
            left_lane[0] = int((left_lane[1] - left_c_x1) / left_lane_avg[4])       # this is the x1 value
            left_lane[2] = int((left_lane[3] - left_c_x2 )/ left_lane_avg[4])       # this is the x2 value
            
            # Now , we have all five values in our left_lane array, x1, y1, x2, y2, and m
            left_lanes_history.append(left_lane)            # We'll store this these values in another array.
       
        if len(right_lines):
            right_lane_avg = np.mean(right_lines, axis = 0)
            # c = y1 - m * x1
            right_c_x1 = right_lane_avg[1] - right_lane_avg[4] * right_lane_avg[0]
            right_c_x2 = right_lane_avg[3] - right_lane_avg[4] * right_lane_avg[2]
            
            # x1 = y1 - c/m
            right_lane[0] = int((right_lane[1] - right_c_x1) / right_lane_avg[4])
            right_lane[2] = int((right_lane[3] - right_c_x2) / right_lane_avg[4])
            
            right_lanes_history.append(right_lane)
            
        if len(left_lanes_history):                                 # if the length of the left_lanes_history is greater than 0
            moving_avg_left_lane = moving_Average(left_lanes_history, 10)
            print("left Lane")
            cv2.line(image, (moving_avg_left_lane[0], moving_avg_left_lane[1]), (moving_avg_left_lane[2], moving_avg_left_lane[3]), [255,0,0], 3 )
    
        if len(right_lanes_history):
            moving_avg_right_lane = moving_Average(right_lanes_history, 10)
            print("right Lane")
            cv2.line(image, (moving_avg_right_lane[0], moving_avg_right_lane[1]), (moving_avg_right_lane[2], moving_avg_right_lane[3]), [255,0,0], 3 )
    except:
        pass
    
    return m
# A little help from pythonProgramming.net
def draw_lines(image, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]),[255,255,255], 1)        # 2nd argument is the position of origin of the line
                                                                                                    # 3rd argument is the position of desination of line.
                                                                                                    # 4rth argument is the color.
                                                                                                    # 5th is the thickness.
                                                                                                            
    except:
        pass
      
def roi(image, vertices):
    # From opencv documentation
    blank_mask = np.zeros_like(image)       # Returns an array of zeros with the same shape and type  as a given array to get started with.
                                            # Here, we are taking the array of the image, and making all its value to zero.
    cv2.fillPoly(blank_mask, vertices, 255) # The function fillPoly fills an area bounded by several polygonal contours.
                                            # here, the blank_mask is our image, vertices is the array of points of polygons
                                            # 255 is the black color.
                                            
    masked_image = cv2.bitwise_and(image, blank_mask)   # For extracting any part of the image, we use bitwise.
    return masked_image

def grayFunction(printscreen_pil):
    
    gray_img = cv2.cvtColor(printscreen_pil, cv2.COLOR_BGR2GRAY)    # Converting the image into gray scale.
    edge_Detection = cv2.Canny(gray_img, 100, 200)                  # taking out only the edges.
    blurred_image = cv2.GaussianBlur(edge_Detection, (5,5), 0)      # To blur the image
    vertices = np.array([[0,540],[0,309],[262,180],[450,180],[750 ,309],[750 ,540]]) 
    
    '''
    How get vertices array from an image?
    Take measurement of the image in centimetre, for eg. the length of the image in cm is 10.5cm.
    and we know, its height in pixels is 540.
    Therefore, for 10.5cm we have 540 pixels,
    which implies, for unit cm, we have 540/10.5.
    Now finding the length, till we have our lane, uing that length(which is 4.5(let say)),
    Then, we have, 4.5 = 540/10.5 * 4.5    (pixels/cm * cm = pixels)
    we get 231(pixels)
    Since we have calculate this distance(4.5) form the bottom, 
    so we have to reduce this result(231) from out height in pixels.
    Which gives us, 540-231 = 309(pixels)
    Simmilarly doing for all the heights and widths, we'll get out vertices array.
    ''' 

    roi_image = roi(blurred_image, [vertices])  
    lines = cv2.HoughLinesP(roi_image,1,np.pi/180,100,20,10)#1st argument is edged image, 2nd is rho, 3rd is delta or the
                                                                        # angle made between the line and the axis, 4rth is minLineLength(The
                                                                        # minimum length of the line, line lesser than  this are rejected.)
                                                                        # 5th is maxLineGap (maximum allowed gap between line segment to treat them as single line)
    m1 = 0
    draw_lines(roi_image, lines)  
    m1 = separate_lines(printscreen_pil,lines)
    
    return roi_image, m1

def csv_file(image_dir, steer_Angle, velocity, throttle):
    print("Writing to csv file!")
    f = open(filename, "w")
    f.write("{}, {}, {}, {}\n".format("Image DIrectory", "Steerring Angle", "Current Velocity", "Throttle"))
    for x in zip(image_dir, steer_Angle, velocity, throttle):
        f.write("{}, {}, {}, {}\n".format(x[0], x[1], x[2], x[3]))
    f.close()
    

arr1=[]
arr2=[]
arr3=[]
splitted_data = []
reply=[]
def socketConnection():
    try:
        data = "1,0"
        sock.sendall(data.encode("utf-8"))          # To send the data
        reply = sock.recv(4096).decode("utf-8")    # To receive the data
        print("Actual data received is: ", reply)
        
        splitted_data = reply.split(',')
        print("after splitting the data: ", splitted_data)
        arr1.append(splitted_data[0])
        arr2.append(splitted_data[1])
        arr3.append(splitted_data[2])
        
    except:
        print("Exception")
    steeringAngle = np.array(arr1) 
    velocity = np.array(arr2)
    throttle = np.array(arr3)
    #csv_file(steeringAngle) this is correct for steering angle.
    return steeringAngle, velocity, throttle

    
local_Address_array = []
while (True):
    num = num + 1
    imageName = str(num) + '.png'      # Name of the images.
    strAngl, vlcty, thrttl = socketConnection()
    printscreen_pil = np.array(ImageGrab.grab(bbox=(0, 120, 750, 540)))          # Taking the screebshot and adding in the array
    image_array = []            # TO store our image in an array.
    
    masked_image, slope = grayFunction(printscreen_pil)


    
    
    '''
    Storing our image in num py array.
    '''
    image_array.append(printscreen_pil)         
    input_image = np.array(image_array)
    
    # Time to itereate through the loop once.
    print("number ",num)#,"   ",  time.time() - firstTime)
    firstTime = time.time()
    
   
    '''
    for storing the image directory location in our csv file.
    '''
    local_Address_array.append(imageName)          # Append each and every directory to LOcal_address_array
    local_address_image = np.array(local_Address_array)     # and then store it in yet another array.
    csv_file(local_address_image, strAngl, vlcty, thrttl)
      
    
    #cv2.imshow('window', cv2.cvtColor(printscreen_pil, cv2.COLOR_BGR2RGB))          # Displaying the image in a window, and convertng the color BGR to RGB
    cv2.imwrite(os.path.join(path, imageName), printscreen_pil)                                       # Trying to save the image in the exact same directory.
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
