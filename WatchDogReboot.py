#from sense_hat import SenseHat, ACTION_PRESSED
from sense_emu import SenseHat, ACTION_PRESSED
from signal import pause
import time
from subprocess import call


sense = SenseHat()
sense.low_light = True
BPM = 90
beatpause = 1/(BPM/60)

green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
pink = (255,105, 180)


def ping():
    P = pink
    O = nothing
    logo = [
    O, O, O, O, O, O, O, O,
    O, P, O, O, O, O, O, O,
    O, O, P, O, O, O, O, O,
    O, O, O, P, O, O, O, O,
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
    O, O, P, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo

images = [ping, pong]


def initiate_reboot():
    sense.show_message("Reboot in", back_colour= blue)
    time.sleep(1)
    sense.show_letter("3", back_colour= blue)
    time.sleep(1)
    sense.show_letter("2", back_colour= blue)
    time.sleep(1)
    sense.show_letter("1", back_colour= blue)
    time.sleep(1)

####
# Main loop
####

while True: 
    sense.set_pixels(ping())
    time.sleep(beatpause)
    sense.set_rotation(90)
    time.sleep(beatpause)
    sense.set_rotation(180)
    time.sleep(beatpause)
    sense.set_rotation(270)
    time.sleep(beatpause)
    sense.set_rotation(0)

#sense.set_pixels(pong())
#    time.sleep(1.00)

    events = sense.stick.get_events()    
    for event in events:
        if event.action == "pressed":
            initiate_reboot() #doesn't pull the trigger though
            call('sudo reboot now', shell=True)

#for event in events:
#   if event.action != "held":            #check if aborted by holding:
#      sense.show_message("aborted", back_colour= red)
#     events = sense.stick.get_events() #clear the event-buffer before going back to main loop
#else:
#  call('sudo reboot now', shell=True)
                    
     
            
