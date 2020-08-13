#!/usr/bin/python3
from sense_hat import SenseHat
#from sense_emu import SenseHat
import time, random

sleeptime_l=1.0
sleeptime_m=sleeptime_l/2
sleeptime_s=sleeptime_m/2
sleeptime_watchtick = 1

s = SenseHat()
s.low_light = True
s.rotation = 90

G = green = (0, 255, 0)
Y = yellow = (255, 255, 0)
B = blue = (0, 0, 255)
R = red = (255, 0, 0)
W = white = (255, 255, 255)
O = nothing = (0, 0, 0)
P = pink = (255,105, 180)

# []

sec_stripeX = [4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3]
sec_stripeY = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0]
sec_stripe_length = len(sec_stripeX)
sec_true = 0  #will effectively be between 1 and 60
sec_LED_current = sec_true*sec_stripe_length/60

watchface_1 = [
    O, O, O, O, O, O, O, O,
    O, O, O, Y, Y, O, O, O,
    O, O, O, O, O, O, O, O,
    O, Y, O, R, R, O, Y, O,
    O, Y, O, R, R, O, Y, O,
    O, O, O, O, O, O, O, O,
    O, O, O, Y, Y, O, O, O,
    O, O, O, O, O, O, O, O,
    ]


# def ping():
#     P = pink
#     O = nothing
#     logo = [
#     O, O, O, O, O, O, O, O,
#     O, O, O, O, O, O, O, O,
#     O, O, O, O, O, O, O, O,
#     O, O, O, O, P, O, O, O,
#     O, O, O, O, O, O, O, O,
#     O, O, O, O, O, O, O, O,
#     O, O, O, O, O, O, O, O,
#     O, O, O, O, O, O, O, O,
#     ]
#     return logo

# 
# images = [ping, pong]


while True: 
    s.set_pixels(watchface_1)
    time.sleep(sleeptime_l)

    localtime = time.localtime(time.time())
    sec_true = localtime.tm_sec
    while sec_true < 60:
        localtime = time.localtime(time.time())
        sec_true = localtime.tm_sec
        sec_LED_current = int(sec_true * (sec_stripe_length / 60))
        sec_stripe_X_LED = int(sec_stripeX[sec_LED_current])
        sec_stripe_Y_LED = int(sec_stripeY[sec_LED_current])
        print(sec_true, ": = LED: ", sec_stripe_X_LED, " - ", sec_stripe_Y_LED)
        s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], blue) 
        s.set_pixel((sec_stripeX[sec_LED_current-2]), sec_stripeY[sec_LED_current-2], nothing)       
        time.sleep(sleeptime_watchtick/2)
        s.set_pixel((sec_stripeX[sec_LED_current-1]), sec_stripeY[sec_LED_current-1], nothing)

s.clear(nothing)