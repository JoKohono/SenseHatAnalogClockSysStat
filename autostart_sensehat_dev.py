#!/usr/bin/python3
# [] <>
# non-sensical insignificant line 2020-08-23 19:17h
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
# from sense_emu import SenseHat
import time
# import random
import psutil
import platform
import inspect
from gpiozero import CPUTemperature
from datetime import datetime
from subprocess import call
import sys


# print(f"Name of the script      : {sys.argv[0]=}")
# print(f"Arguments of the script : {sys.argv[1:]=}")

# log_level = ("NONE", "INFO", "ERROR", "DEBUG")
loglevel_deep = True
tick_launch = time.time()


def ticker():
    delta_t = time.time() - tick_launch
    ticker_x = f'{delta_t:.3f}:'
    debug_time = time.localtime(time.time())
    ticker_x = str(ticker_x)+(" ")+str(time.asctime())+(" ")
    return ticker_x


sleeptime_l = 1.0
sleeptime_m = sleeptime_l/2
sleeptime_s = sleeptime_l/4
sleeptime_watchtick = 1



s = SenseHat()
s.low_light = False
s.rotation = 90

nightmode = False

G = green = [0, 255, 0]
g = green_low = [0, 100, 0]
Y = yellow = [255, 255, 0]
y = yellow_low = [100, 100, 0]
B = blue = [0, 0, 255]
b = blue_low = [0, 0, 100]
R = red = [255, 0, 0]
r = red_low = [100, 0, 0]
W = white = [255, 255, 255]
w = white_low = [100, 100, 100]
O = nothing = [0,0,0]
P = pink = [255,105, 180]


#------------Seconds------------------------------------
# smiley center to out 4 pixel
sec_stripeX = [3, 4, 2, 5]
sec_stripeY = [5, 5, 4, 4]
sec_stripe_pixelcolor = [B, G, Y, ]
# symmetric smiley center to out 2 twice per minute
#sec_stripeX = [3, 4, 2, 5, 3, 4, 2, 5]
#sec_stripeY = [5, 5, 4, 4, 5, 5, 5, 5]

sec_stripe_length = len(sec_stripeX)
sec_true = 0  #will effectively be between 1 and 60
sec_LED_current = sec_true*sec_stripe_length/60
sec_LED_old = 0
sec_pixel_color = G

# ------------Minutes-----------------------------------
min_stripeX = [4,5,6,6,6,6,6,6,5,4,3,2,1,1,1,1,1,1,2,3]
min_stripeY = [1,1,1,2,3,4,5,6,6,6,6,6,6,5,4,3,2,1,1,1]
min_stripe_length = len(min_stripeX)
min_true = 0  #will effectively be between 1 and 60
min_LED_current = min_true*min_stripe_length/60

# ------------Hours-----------------------------------------------
hour_stripeX =            [3,2,1,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,7,7,7,7,7,7,7,6,5,4]
hour_stripeY =            [7,7,7,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,7,7,7]
hour_stripe_color_day =   [B,B,B,B,B,B,G,G,Y,R,R,R,R,R,R,R,R,R,R,R,Y,G,G,G,G,G,B,B]
hour_stripe_color_night = [O,O,O,b,O,O,O,O,O,O,r,O,O,O,O,O,O,r,O,O,O,O,O,O,g,O,O,O]
hour_stripe_color = hour_stripe_color_day
hour_stripe_length = len(hour_stripeX)
hour_true = 0  #will effectively be between 1 and 24
hour_LED_current = hour_true*hour_stripe_length/24



#--------Watchface and Maintenance---------------------------------------------

def night_or_day():
    tfn = inspect.currentframe().f_code.co_name
    localtime = time.localtime(time.time())
    hour_true = localtime.tm_hour
#    hour_true = 23  #to force night mode for testing purpose
    if hour_true < 6 or hour_true > 20:
        nightmode = True
        s.low_light = True
        hour_stripe_color = hour_stripe_color_night
        if loglevel_deep: print(ticker(), "(",tfn,")", "--night-or-day says: night")
        return(hour_stripe_color)
    else:
        nightmode = False
        s.low_light = False
        hour_stripe_color = hour_stripe_color_day
        if loglevel_deep: print(ticker(), "(",tfn,")", "--night-or-day says: day")
        return(hour_stripe_color)

def wipe_sec_stripe():
    tfn=inspect.currentframe().f_code.co_name 
    for pixel in range(sec_stripe_length):
        s.set_pixel(sec_stripeX[pixel], sec_stripeY[pixel], nothing)
    if loglevel_deep: print(ticker(),"(",tfn,")", "wiped the second-strip")
    return()

def min_wipe_stripe():
    tfn=inspect.currentframe().f_code.co_name 
    for pixel in range(min_stripe_length):
        s.set_pixel(min_stripeX[pixel], min_stripeY[pixel], nothing)
    if loglevel_deep: print(ticker(),"(",tfn,")", "min_wipe_stripe has wiped the minute-strip")
    return()

def hour_wipe_stripe():
    tfn=inspect.currentframe().f_code.co_name 
    for pixel in range (hour_stripe_length):
        s.set_pixel(hour_stripeX[pixel], hour_stripeY[pixel], hour_stripe_color[pixel])
    if loglevel_deep: print(ticker(),"(",tfn,")", "hour_wipe_stripe has initialized the hour-strip")
    return()

def get_hour_pixel():
    tfn=inspect.currentframe().f_code.co_name 
    pixel_1 = (0,0)
    pixel_2 = (1,1)   #these coordinates are invalid. I'm returning this for pixel2 to tell the caller that there is no pixel_2
    localtime = time.localtime(time.time())
    hour_true = localtime.tm_hour
    if hour_true < 10:
        pixel_1 = (hour_stripeX[hour_true],hour_stripeY[hour_true])
    elif hour_true == 10:
        pixel_1=(hour_stripeX[hour_true],hour_stripeY[hour_true])
        pixel_2=(hour_stripeX[hour_true+1],hour_stripeY[hour_true+1])
    elif hour_true == 11:
        pixel_1 = (hour_stripeX[hour_true+1],hour_stripeY[hour_true+1])
        pixel_2=(hour_stripeX[hour_true+2],hour_stripeY[hour_true+2])
    elif hour_true == 12:
        pixel_1 =(hour_stripeX[hour_true+2],hour_stripeY[hour_true+2])
        pixel_2=(hour_stripeX[hour_true+3],hour_stripeY[hour_true+3])
    elif hour_true == 13:
        pixel_1 = (hour_stripeX[hour_true+3],hour_stripeY[hour_true+3])
        pixel_2=(hour_stripeX[hour_true+4],hour_stripeY[hour_true+4])
    elif hour_true > 13:
        # add the 4 redundant top row pixel
        pixel_1 = (hour_stripeX[hour_true+4],hour_stripeY[hour_true+4])
    if loglevel_deep: print(ticker(),"(",tfn,")", "hour pixel(s): ", pixel_1, pixel_2)
    return (pixel_1, pixel_2)


#--------------System-----------------------------------------
CPU_pixel = (2,2)
IO_pixel = (5,2)
#IO_pixel_rx = (2,2) 
#IO_pixel_tx = (5,2)

CPU_load_hard_high = 90
CPU_load_high = 60
CPU_load_medium = 35
CPU_load_low = 10

CPU_f_overclock = 1500
CPU_f_full = 800
CPU_f_reduced_medium = 650
CPU_f_minimum = 600 

Temp_hard_high = 80
Temp_high = 54
Temp_medium = 45

Mem_hard_high = 90  #numbers are percent memory utilization
Mem_high =      75
Mem_medium =    35

IO_sent = 0
IO_received = 0
delta_IO_rx_red = 100
delta_IO_rx_yellow = 5000
delta_IO_rx_green = 15000
delta_IO_rx_blue =500000

delta_IO_tx_red = 100
delta_IO_tx_yellow = 5000
delta_IO_tx_green = 15000
delta_IO_tx_blue =500000

delta_IO_red = 100
delta_IO_yellow = 5000
delta_IO_green = 15000
delta_IO_blue =500000

def update_system():
    tfn=inspect.currentframe().f_code.co_name 
    #CPU Pixel----------------------------------------------
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
    if loglevel_deep: print(ticker(),"(",tfn,")", "CPU load is: ", CPU_load)
    
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
    if loglevel_deep: print(ticker(),"(",tfn,")", "CPU freq. is: ", cpufreq.current)

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
    if loglevel_deep: print(ticker(),"(",tfn,")", "CPU temp. is: ", cpu.temperature)
        
    #CPU Memory--------------------------
    svmem = psutil.virtual_memory()
    if svmem.percent > 95:
        tfn=inspect.currentframe().f_code.co_name
        if loglevel_deep: print(ticker(),"(",tfn,")", "system will be rebootet because of low memory")
        call('sudo reboot now', shell=True)
    if svmem.percent  >  Mem_hard_high:
        Mem_color = red
    elif svmem.percent   >  Mem_high:
        Mem_color = yellow
    elif svmem.percent   >  Mem_medium:
        Mem_color = green
    else:
        Mem_color = blue
    if loglevel_deep: print(ticker(),"(",tfn,")", "Memory utilization is: ", svmem.percent)

    # determine the aggregated single LED for CPU: 
    if (svmem.percent > Mem_hard_high) or (cpu.temperature > Temp_hard_high) or ((cpufreq.current < CPU_f_full) and (CPU_load > CPU_load_hard_high)):
        CPU_color = red
    elif (svmem.percent > Mem_high) or (cpu.temperature > Temp_high) or ((cpufreq.current == CPU_f_full) and (CPU_load > CPU_load_high)):
        CPU_color = yellow
    elif (CPU_load < CPU_load_medium) and (cpu.temperature < Temp_high) and (svmem.percent < Mem_medium):
        CPU_color = blue
    else:
        CPU_color = green

    if loglevel_deep: print(ticker(),"(",tfn,")", "the CPU LED is: ", CPU_pixel, CPU_color)
    s.set_pixel(CPU_pixel[0], CPU_pixel[1], CPU_color)               


    global IO_sent
    global IO_received

    IO_sent_old = IO_sent
    IO_received_old = IO_received
    net_io = psutil.net_io_counters()
    IO_sent = net_io.bytes_sent
    IO_received = net_io.bytes_recv
    delta_IO_tx = IO_sent - IO_sent_old
    delta_IO_rx = IO_received - IO_received_old
    delta_IO = delta_IO_rx + delta_IO_tx
#    if loglevel_deep: print(ticker(), "delta sent: ", delta_IO_tx)
#    if loglevel_deep: print(ticker(), "delta recv: ", delta_IO_rx)
    if loglevel_deep: print(ticker(),"(",tfn,")", "delta IO: ", delta_IO)


    if delta_IO > delta_IO_blue: IO_color = blue
    elif delta_IO > delta_IO_green: IO_color = green
    elif delta_IO > delta_IO_yellow: IO_color = yellow
    elif delta_IO > delta_IO_red: IO_color = red
    else: IO_color = white
    s.set_pixel(IO_pixel[0], IO_pixel[1], IO_color)
    if loglevel_deep: print(ticker(),"(",tfn,")", "IO_color is: ", IO_color)

#     if delta_IO_rx > delta_IO_rx_blue: IO_rx_color = white
#     elif delta_IO_rx > delta_IO_rx_green: IO_rx_color = green
#     elif delta_IO_rx > delta_IO_rx_yellow: IO_rx_color = yellow
#     elif delta_IO_rx > delta_IO_rx_red: IO_rx_color = red
#     else: IO_rx_color = red
#     if loglevel_deep: print(ticker(), "-- IO_rx_coloer is: ", IO_rx_color)
#     s.set_pixel(IO_pixel_rx[0], IO_pixel_rx[1], IO_rx_color)    

    return() 
#End of System Pixel Block------------    

# ----------- Joystick & Rebooting -----------


def initiate_reboot():
    s.show_message("Reboot in", back_colour= blue)
    time.sleep(1)
    s.show_letter("3", back_colour= blue)
    time.sleep(1)
    s.show_letter("2", back_colour= blue)
    time.sleep(1)
    s.show_letter("1", back_colour= blue)
    time.sleep(1)


def check_joystick():
    tfn = inspect.currentframe().f_code.co_name
    events = s.stick.get_events()
    for event in events:
        if event.action == "pressed":
            if loglevel_deep: print(ticker(), "(", tfn, ")", "joystick-pressed-event detected and will reboot now")
            initiate_reboot()   # doesn't pull the trigger yet - just the countdown
            call('sudo reboot now', shell=True)


# -------------- Main Program -----------------------------------------------------
# ------------- and execute... ----------------------------------------------------
while True: 
    for i in range(8):     #clear the entire display
        for ii in range(8):
            s.set_pixel(i, ii, nothing)
    time.sleep(sleeptime_m)      
    hour_stripe_color=night_or_day()

#    hour_wipe_stripe()     #initialize the hour stripe
#    if loglevel_deep: print(ticker(),"display cleared and hour ring initialized before going into 24-hour loop")

    localtime = time.localtime(time.time())
    hour_true = localtime.tm_hour
    
    while hour_true < 24:
        hour_wipe_stripe()     #initialize the hour stripe
        if loglevel_deep: print(ticker(),"display cleared and hour ring initialized from inside 24hr loop")
        localtime = time.localtime(time.time())
        hour_true = localtime.tm_hour        
        hour_LED_current = get_hour_pixel()
        if loglevel_deep: print(ticker(),"true hour: ", hour_true, "  LED coordinates: ", hour_LED_current)
      
        #blank the hour_LED to give the SECONDS-loop a clean start with turning it back on
        x = (hour_LED_current[0])[0]
        y = (hour_LED_current[0])[1]
        s.set_pixel(x, y, nothing)
        if loglevel_deep: print(ticker(),"in the hour loop, turn off hour LED now at: ",x, y)
        if hour_LED_current[1] != (1,1):
            x = (hour_LED_current[1])[0]
            y = (hour_LED_current[1])[1]
            s.set_pixel(x, y, nothing)
            if loglevel_deep: print(ticker(),"detected a 2pixel and turned off 2ndLED now at: ",x, y)

        
        
        #---- MINUTES LOOP ----------------------------------------------
        min_wipe_stripe()
        while min_true < 59:
            localtime = time.localtime(time.time())
            min_true = localtime.tm_min
            if loglevel_deep: print(ticker(),"beginning of minute-loop, showing min_true: ", min_true)
            hour_stripe_color=night_or_day()

            min_LED_current = int(min_true * (min_stripe_length / 60))
            min_stripe_X_LED = int(min_stripeX[min_LED_current])
            min_stripe_Y_LED = int(min_stripeY[min_LED_current])
            s.set_pixel((min_stripeX[min_LED_current]), min_stripeY[min_LED_current], nothing) 
            s.set_pixel((min_stripeX[min_LED_current-1]), min_stripeY[min_LED_current-1], nothing) 


            #---- SECONDS LOOP ----------------------------------------------
            sec_true = localtime.tm_sec
            while sec_true < 59:
                #-----take care of SECONDS---------------
                check_joystick()
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
                hour_LED_current = get_hour_pixel()
                if loglevel_deep: print(ticker(),"toggling the hour-LED now:")
                if loglevel_deep: print(ticker(),"the current hour: ", hour_LED_current, "vs. true hour: ",hour_true)
                x = (hour_LED_current[0])[0]
                y = (hour_LED_current[0])[1]
                if s.get_pixel(x, y) == [0, 0, 0]:
                    was_off = True
                else:
                    was_off = False
                
                if was_off:
                    s.set_pixel(x, y, pink)          
#                    s.set_pixel(x, y, hour_stripe_color[hour_true])          
                    if loglevel_deep: print(ticker(),"turned ON  hour LED x,y now: ",x, y)
                    if hour_LED_current[1] != (1,1):
                        x = (hour_LED_current[1])[0]
                        y = (hour_LED_current[1])[1]
                        s.set_pixel(x, y, pink)      
#                        s.set_pixel(x, y, hour_stripe_color[hour_true])      
                        if loglevel_deep: print(ticker(),"turned ON  2nd hour LED x,y now: ",x, y)
                else:
                    s.set_pixel(x, y, nothing)
                    if loglevel_deep: print(ticker(),"turned OFF hour LED x,y now: ",x, y)
                    if hour_LED_current[1] != (1,1):
                        x = (hour_LED_current[1])[0]
                        y = (hour_LED_current[1])[1]
                        s.set_pixel(x, y, nothing)
                        if loglevel_deep: print(ticker(),"turned OFF 2nd hour LED x,y now: ",x, y)
                    
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
                if loglevel_deep: print(ticker(),"sec: ", sec_true)
                

            #to avoid unnecessary loops in the minutes and hours
            time.sleep(sleeptime_watchtick/2)
            sec_true = 0
        
        min_true = 0
    
