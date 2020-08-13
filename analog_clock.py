from sense_hat import SenseHat
#from sense_emu import SenseHat
import time, random

sleeptime_l=1.0
sleeptime_m=sleeptime_l/2
sleeptime_s=sleeptime_m/2

s = SenseHat()
s.low_light = True
s.rotation = 90

green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
nothing = (0, 0, 0)
pink = (255,105, 180)

# []

sec_stripeX = [4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3]
sec_stripeY = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0]
sec_stripe_length = len(sec_stripeX)
sec_true = 0  #will effectively be between 1 and 60
sec_LED_current = sec_true*sec_stripe_length/60

def secondsarray():
    off = nothing
    on = yellow
    secondslogo =[
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, P, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return secondslogo

def ping():
    P = pink
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, P, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo

def pong():
    P = pink
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, P, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo

images = [ping, pong]
count = 0

while True: 
#    s.set_pixels(images[count % len(images)]())
#    time.sleep(sleeptime_m)

    s.clear(nothing)
    sec_true = 0
    while sec_true < 60:
        sec_LED_current = int(sec_true * (sec_stripe_length / 60))
        sec_stripe_X_LED = int(sec_stripeX[sec_LED_current])
        sec_stripe_Y_LED = int(sec_stripeY[sec_LED_current])
        print(sec_true)
        print(sec_stripe_X_LED, " - ", sec_stripe_Y_LED)
        s.set_pixel((sec_stripeX[sec_LED_current]), sec_stripeY[sec_LED_current], blue)

        time.sleep(sleeptime_l)
        sec_true += 1

#   count += 1
s.clear(nothing)