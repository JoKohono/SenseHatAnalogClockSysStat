import time
# <> [] {} @ ~/|\

while True:
    localtime = time.localtime(time.time())
#    print("Local current time :", localtime)

    sec_true = localtime.tm_sec
    print("true second: ", sec_true)
    time.sleep(1)
    