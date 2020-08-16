#!/usr/bin/python3
# [] <>
from sense_hat import SenseHat
#from sense_emu import SenseHat
import time, random
import psutil
import platform
from gpiozero import CPUTemperature
from datetime import datetime


sleeptime_l=1.0
sleeptime_m=sleeptime_l/2
sleeptime_s=sleeptime_m/2
sleeptime_watchtick = 1

s = SenseHat()
s.low_light = False
s.rotation = 90

nightmode = False

G = green = [0, 255, 0]
Y = yellow = [255, 255, 0]
y = yellow_low = [100, 100, 0]
b = blue_low = [0, 0, 100]
B = blue = [0, 0, 255]
R = red = [255, 0, 0]
W = white = [255, 255, 255]
O = nothing = [0,0,0]
P = pink = [255,105, 180]


#------------Seconds------------------------------------
sec_stripeX = [2, 3, 4, 5]
sec_stripeY = [5, 5, 5, 5]
sec_stripe_length = len(sec_stripeX)
sec_true = 0  #will effectively be between 1 and 60
sec_LED_current = sec_true*sec_stripe_length/60
sec_LED_old = 0
sec_pixel_color = green

#------------Minutes-----------------------------------
min_stripeX = [4,5,6,6,6,6,6,6,5,4,3,2,1,1,1,1,1,1,2,3]
min_stripeY = [1,1,1,2,3,4,5,6,6,6,6,6,6,5,4,3,2,1,1,1]
min_stripe_length = len(min_stripeX)
min_true = 0  #will effectively be between 1 and 60
min_LED_current = min_true*min_stripe_length/60

#------------Hours-----------------------------------------------
hour_stripeX =      [3,2,1,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,7,7,7,7,7,7,7,6,5,4]
hour_stripeY =      [7,7,7,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,7,7,7]
hour_stripe_color = [B,B,B,B,B,B,G,G,G,R,R,R,R,R,R,R,R,R,R,R,R,G,G,G,G,G,B,B]
hour_stripe_length = len(hour_stripeX)
hour_true = 0  #will effectively be between 1 and 24
hour_LED_current = hour_true*hour_stripe_length/24


    


#--------Watchface and Maintenance---------------------------------------------

def night_or_day():
    localtime = time.localtime(time.time())
    hour_true = localtime.tm_hour
    if hour_true < 6 or hour_true > 21:
        nightmode = True
        s.low_light = True
        G = green = [0, 100, 0]
        Y = yellow = [100, 100, 0]
        B = blue = [0, 0, 100]
        R = red = [100, 0, 0]
        W = white = [100, 100, 100]        
    else:
        nightmode = False
        s.low_light = False
        G = green = [0, 255, 0]
        Y = yellow = [255, 255, 0]
        y = yellow_low = [100, 100, 0]
        b = blue_low = [0, 0, 100]
        B = blue = [0, 0, 255]
        R = red = [255, 0, 0]
        W = white = [255, 255, 255]
        P = pink = [255,105, 180]
    

def wipe_sec_stripe():
    for pixel in range(sec_stripe_length):
        s.set_pixel(sec_stripeX[pixel], sec_stripeY[pixel], nothing)
    return()

def min_wipe_stripe():
    for pixel in range(min_stripe_length):
        s.set_pixel(min_stripeX[pixel], min_stripeY[pixel], nothing)
    return()   

def hour_wipe_stripe():
    for pixel in range (hour_stripe_length):
        s.set_pixel(hour_stripeX[pixel], hour_stripeY[pixel], hour_stripe_color[pixel])
    return()

def get_hour_pixel(hour_true):
    pixel_1 = (0,0)
    pixel_2 = (1,1)   #these coordinates are invalid. I'm returning this for pixel2 to tell the caller that there is no pixel_2
    if hour_true < 10:
        pixel_1 = (hour_stripeX[hour_true],hour_stripeY[hour_true])
        return (pixel_1, pixel_2)
    elif hour_true == 10:
        pixel_1=(hour_stripeX[hour_true],hour_stripeY[hour_true])
        pixel_2=(hour_stripeX[hour_true+1],hour_stripeY[hour_true+1])
        return (pixel_1, pixel_2)
    elif hour_true == 11:
        pixel_1 = (hour_stripeX[hour_true+1],hour_stripeY[hour_true+1])
        pixel_2=(hour_stripeX[hour_true+2],hour_stripeY[hour_true+2])
        return (pixel_1, pixel_2)
    elif hour_true == 12:
        pixel_1 =(hour_stripeX[hour_true+2],hour_stripeY[hour_true+2])
        pixel_2=(hour_stripeX[hour_true+3],hour_stripeY[hour_true+3])
        return (pixel_1, pixel_2)    
    elif hour_true == 13:
        pixel_1 = (hour_stripeX[hour_true+3],hour_stripeY[hour_true+3])
        pixel_2=(hour_stripeX[hour_true+4],hour_stripeY[hour_true+4])
    elif hour_true > 13:
        # add the 4 redundant top row pixel
        pixel_1 = (hour_stripeX[hour_true+4],hour_stripeY[hour_true+4])
        return (pixel_1, pixel_2)



#--------------System-----------------------------------------
CPU_load_color = white
CPU_load_hard_high = 85
CPU_load_high = 60
CPU_load_medium = 25
CPU_load_low = 10
CPU_load_pixel = (2,2,CPU_load_color)


CPU_f_color = white
CPU_f_overclock = 1500
CPU_f_full = 800
CPU_f_reduced_medium = 650
CPU_f_minimum = 600 
CPU_f_pixel = (3,2,CPU_f_color)

Temp_color = white
Temp_hard_high = 80
Temp_high = 55
Temp_medium = 45
Temp_pixel = (4,2,Temp_color)

Mem_color = white
Mem_hard_high = 75  #numbers are percent memory utilization
Mem_high =      35
Mem_medium =    10
Mem_pixel = (5,2,Mem_color)

eth_color = white
wlan0_color = white
wg0_color = white
io_color = white


def update_system():
    #System Pixel----------------------------------------------
    #CPU load----------------------------
    CPU_load = int(psutil.cpu_percent())
    if CPU_load  > CPU_load_hard_high:
        CPU_load_color = red
    elif CPU_load  > CPU_load_high:
        CPU_load_color = yellow
    elif CPU_load  > CPU_load_medium:
        CPU_load_color = green
    else:
        CPU_load_color = blue
    
    #CPU frequency-----------------------
    cpufreq = psutil.cpu_freq()
    if cpufreq.current > CPU_f_overclock:
        CPU_f_color = red
    elif cpufreq.current > CPU_f_full:
        CPU_f_color = yellow
    elif cpufreq.current > CPU_f_reduced_medium:
        CPU_f_color = green
    else:
        CPU_f_color = blue
    #CPU temperature---------------------
    cpu = CPUTemperature()
    if (cpu.temperature) > Temp_hard_high:
        Temp_color = red
    elif cpu.temperature  >  Temp_high:
        Temp_color = yellow
    elif cpu.temperature  >  Temp_medium:
        Temp_color = green
    else:
        Temp_color = blue
    #CPU Memory--------------------------
    svmem = psutil.virtual_memory()
    if svmem.percent  >  Mem_hard_high:
        Mem_color = red
    elif svmem.percent   >  Mem_high:
        Mem_color = yellow
    elif svmem.percent   >  Mem_medium:
        Mem_color = green
    else:
        Mem_color = blue
    
    s.set_pixel(2,2,CPU_load_color)                
    s.set_pixel(3,2,CPU_f_color)
    s.set_pixel(4,2,Temp_color)
    s.set_pixel(5,2,Mem_color)
    return()    
    #End of System Pixel Block------------    


#---------------------------------------------------------------------------------
#------------- and execute... ----------------------------------------------------

while True: 
    for i in range(8):     #clear the entire display
        for ii in range(8):
            s.set_pixel(i, ii, nothing)
    night_or_day()

    hour_wipe_stripe()     #initialize the hour stripe
    print("display cleared and hour ring initialized")

    localtime = time.localtime(time.time())
    hour_true = localtime.tm_hour
    
    while hour_true < 24:
        hour_true = localtime.tm_hour
        hour_LED_current = get_hour_pixel(hour_true)
        print("true hour: ", hour_true, "     LED coord: ", hour_LED_current)
      
        #blank the hour_LED to give the SECONDS-loop a clean start with turning it back on
        x = (hour_LED_current[0])[0]
        y = (hour_LED_current[0])[1]
        s.set_pixel(x, y, nothing)
        print("blanked LED x,y now: ",x, y)
        if hour_LED_current[1] != (1,1):
            x = (hour_LED_current[1])[0]
            y = (hour_LED_current[1])[1]
            s.set_pixel(x, y, nothing)
            print("detected a 2pixel and blanked 2ndLED x,y now: ",x, y)

        
        
        #---- MINUTES LOOP ----------------------------------------------
        min_wipe_stripe()
        while min_true < 59:
            localtime = time.localtime(time.time())
            min_true = localtime.tm_min
            night_or_day()

            min_LED_current = int(min_true * (min_stripe_length / 60))
            min_stripe_X_LED = int(min_stripeX[min_LED_current])
            min_stripe_Y_LED = int(min_stripeY[min_LED_current])
            s.set_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current], nothing) 
            s.set_pixel((min_stripeX[min_LED_current-1]), min_stripeY[min_LED_current-1], nothing) 


            #---- SECONDS LOOP ----------------------------------------------
            sec_true = localtime.tm_sec
            while sec_true < 59:
                #-----take care of SECONDS---------------
                localtime = time.localtime(time.time())
                sec_true = localtime.tm_sec
                sec_LED_current = int(sec_true * (sec_stripe_length / 60))
                sec_stripe_X_LED = int(sec_stripeX[sec_LED_current])
                sec_stripe_Y_LED = int(sec_stripeY[sec_LED_current])
             
                if sec_LED_current > sec_LED_old:   #make sure the previous LED in the stripe is left ON
                    s.set_pixel((sec_stripeX[sec_LED_old]), sec_stripeY[sec_LED_old], sec_pixel_color)
                elif sec_LED_current < sec_LED_old:   # means: we must have a new minute
                    wipe_sec_stripe()

#on comment for now to try to stop seconds from blinking
#                 if (s.get_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current])) == nothing:
                s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], sec_pixel_color)      
#                 else:
#                     s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], nothing) 

                
                #--now toggle on the hour-LED------------------
                hour_LED_current = get_hour_pixel(hour_true)
                x = (hour_LED_current[0])[0]
                y = (hour_LED_current[0])[1]
                if s.get_pixel(x, y) == [0, 0, 0]:
                    was_off = True
                else:
                    was_off = False
                
                if was_off:
                    s.set_pixel(x, y, pink)          
#                    s.set_pixel(x, y, hour_stripe_color[hour_true])          
                    print("turned on hour LED x,y now: ",x, y)
                    if hour_LED_current[1] != (1,1):
                        x = (hour_LED_current[1])[0]
                        y = (hour_LED_current[1])[1]
                        s.set_pixel(x, y, pink)      
#                        s.set_pixel(x, y, hour_stripe_color[hour_true])      
                        print("turned on 2nd hour LED x,y now: ",x, y)
                else:
                    s.set_pixel(x, y, nothing)
                    if hour_LED_current[1] != (1,1):
                        x = (hour_LED_current[1])[0]
                        y = (hour_LED_current[1])[1]
                        s.set_pixel(x, y, nothing)
                    
                #------and also blink the minute pixel
                if s.get_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current]) != [0,0,0]:
                    s.set_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current], nothing)
                else:
                    s.set_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current], pink)                                    
                        
                
                #------update the SYSTEM LEDs-----------
                update_system()
                time.sleep(sleeptime_watchtick/2)
                
                #-------part of seconds blinking---------
#                 if (s.get_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current])) == nothing:
#                     s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], sec_pixel_color)      
#                 else:
#                     s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], nothing) 
                time.sleep(sleeptime_watchtick/2)
#                 if (s.get_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current])) == nothing:
#                     s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], sec_pixel_color)      
#                 else:
#                     s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], nothing) 
                sec_LED_old = sec_LED_current
                print("sec: ", sec_true)
                

            #to avoid unnecessary loops in the minutes and hours
            time.sleep(sleeptime_watchtick/2)
            sec_true = 0
        
        min_true = 0
    
