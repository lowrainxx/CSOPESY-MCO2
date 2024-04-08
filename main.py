import threading
import os

super_citizen_semaphore = threading.Semaphore(2) # at least 1, at most 2
regular_citizen_semaphore = threading.Semaphore(3) # at least 2, at most 3
team_lock = threading.Lock()

# Waiting queue counter
super_citizens_waiting = 0
regular_citizens_waiting = 0

def super_citizen():
    print("Super Citizen signing up\n")

def regular_citizen():
    print("Regular Citizen signing up\n")

# Signup queue
def simulate_signup():
    threads = []

    t1 = threading.Thread(target=super_citizen, name='t1')
    t2 = threading.Thread(target=regular_citizen, name='t2')
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()

global r, s
r = input("Input the total number of regular citizens: ")
s = input("Input the total number of super citizens: ")

if(r > 0 and s >= 0):
      simulate_signup()

print("\n----------DONE----------\n")

# print("ID of process running main program: {}".format(os.getpid()))