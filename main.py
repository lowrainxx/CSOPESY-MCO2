import threading

super_citizen_semaphore = threading.Semaphore(2) # at least 1, at most 2
regular_citizen_semaphore = threading.Semaphore(3) # at least 2, at most 3
team_lock = threading.Lock()

# Waiting queue counter
super_citizens_waiting = 0
regular_citizens_waiting = 0

def super_citizen():
    pass

def regular_citizen():
    pass

# Signup queue
def signups():
    threads = []
    for _ in range(s):
        t = threading.Thread(target=super_citizen)
        threads.append(t)
        t.start()

    for _ in range(r):
        t = threading.Thread(target=regular_citizen)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

global r, s
r = input("Input the total number of regular citizens: ")
s = input("Input the total number of super citizens: ")

signups()