#file object = open("local_mailbox".txt [, r+][, buffering])

# Open a file
config_file = open("config.txt", "r+")


print ("Name of the file: ", config_file.name)
print ("Closed or not : ", config_file.closed)
print ("Opening mode : ", config_file.mode)

config_file.close()
