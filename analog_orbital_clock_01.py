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
Bl= blue_low = [0, 0, 100]
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
hour_true = 0
hour_stripeX = [4,5,6,6,6,6,6,6,5,4,3,2,1,1,1,1,1,1,2,3]
hour_stripeY = [1,1,1,2,3,4,5,6,6,6,6,6,6,5,4,3,2,1,1,1]
hour_stripe_length = len(hour_stripeX)
hour_true = 0  #will effectively be between 1 and 24
hour_LED_current = hour_true*hour_stripe_length/24




#--------Watchface and Maintenance---------------------------------------------
watchface_orbit_day = [
    R, R, R, R, R, R, R, R,
    R, O, O, O, O, O, O, R,
    R, O, O, O, O, O, O, R,
    G, O, O, O, O, O, O, R,
    G, O, O, O, O, O, O, G,
    B, O, O, O, O, O, O, G,
    B, O, O, O, O, O, O, G,
    B, B, B, B, B, B, B, G, 
    ]
watchface_orbit_night = [
    R, O, O, O, O, O, O, R,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    B, O, O, O, O, O, O, G, 
    ]

def wipe_sec_stripe():
    for pixel in range(sec_stripe_length):
        s.set_pixel(sec_stripeX[pixel], sec_stripeY[pixel], nothing)
    return()

def min_wipe_stripe():
    for pixel in range(min_stripe_length):
        s.set_pixel(min_stripeX[pixel], min_stripeY[pixel], nothing)
    return()   


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
if not nightmode:
    s.set_pixels(watchface_orbit_day)
else:
    s.set_pixels(watchface_orbit_night)
    
while True: 
    localtime = time.localtime(time.time())
    hour_true = localtime.tm_hour
    while hour_true < 23:
        min_wipe_stripe()
        while min_true < 59:
            localtime = time.localtime(time.time())
            min_true = localtime.tm_min

            #todo later: set low-light based on actual sunrise/sunset
            if hour_true > 21 or hour_true < 6:
                s.low_light = True
            else:
                s.low_light = False
            #-------------------------------------------------------//

            min_LED_current = int(min_true * (min_stripe_length / 60))
            min_stripe_X_LED = int(min_stripeX[min_LED_current])
            min_stripe_Y_LED = int(min_stripeY[min_LED_current])
#            print(min_true, ": = LED: ", min_stripe_X_LED, " - ", min_stripe_Y_LED)

            old_pixel0 = s.get_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current]) 
            old_pixel1 = s.get_pixel((min_stripeX[min_LED_current-1]), min_stripeY[min_LED_current]-1) 
#            old_pixel2 = s.get_pixel((min_stripeX[min_LED_current-2]), min_stripeY[min_LED_current]-2) 
#            print("op0: ", old_pixel0)
#            print("op1: ", old_pixel1)
#            print("op2: ", old_pixel2)
            s.set_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current], yellow) 
#            s.set_pixel((min_stripeX[min_LED_current-2]), min_stripeY[min_LED_current-2], old_pixel2)       
            time.sleep(sleeptime_watchtick/2)
            s.set_pixel((min_stripeX[min_LED_current-1]), min_stripeY[min_LED_current-1], old_pixel1)



            sec_true = localtime.tm_sec
            while sec_true < 59:
                localtime = time.localtime(time.time())
                sec_true = localtime.tm_sec
                sec_LED_current = int(sec_true * (sec_stripe_length / 60))
                sec_stripe_X_LED = int(sec_stripeX[sec_LED_current])
                sec_stripe_Y_LED = int(sec_stripeY[sec_LED_current])
             
                if sec_LED_current > sec_LED_old:   #make sure the previous LED in the stripe is left ON
                    s.set_pixel((sec_stripeX[sec_LED_old]), sec_stripeY[sec_LED_old], sec_pixel_color)
                elif sec_LED_current < sec_LED_old:   # means: we must have a new minute
                    wipe_sec_stripe()
                    
                if (s.get_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current])) == nothing:
                    s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], sec_pixel_color)      
                else:
                    s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], nothing) 
                
                update_system()
                time.sleep(sleeptime_watchtick/2)
                
                if (s.get_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current])) == nothing:
                    s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], sec_pixel_color)      
                else:
                    s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], nothing) 
                time.sleep(sleeptime_watchtick/4)
                if (s.get_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current])) == nothing:
                    s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], sec_pixel_color)      
                else:
                    s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], nothing) 
                sec_LED_old = sec_LED_current
            #to avoid unnecessary loops in the minutes and hours
            time.sleep(sleeptime_watchtick/2)
            sec_true = 0
        
        min_true = 0
    
