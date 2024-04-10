from threading import Thread, Semaphore, Lock
import random 
import time

'''
TERMS:
threading.Thread() = returns thread object
    daemon = True if thread should exit when program exits
                  else False
Thread.start() =
Thread.join() =
threading.Semaphore() = to limit number of threads
Semaphore.acquire() = acquire semaphore
Semaphore.release() = release semaphore
    blocking = False if thread will not block if semaphore isnt available
                     else True
threading.Lock() =
'''

class Helldivers:
    def __init__(self, r, s):
        self.r = r
        self.s = s 
        self.team_id = 0
        self.sc_id = 0
        self.rc_id = 0
        self.regular_queue = Semaphore(1)
        self.super_queue = Semaphore(1)
        self.lock = Lock()
        self.total_teams_sent = 0
        self.unsent_rc = r
        self.unsent_sc = s

    def regular_citizen(self):
        for _ in range(self.r):
            time.sleep(random.uniform(0.1, 0.5))  # Simulate queueing time
            self.regular_queue.release()

    def super_citizen(self):
        for _ in range(self.s):
            time.sleep(random.uniform(0.1, 0.5))  # Simulate queueing time
            self.super_queue.release()
    
    def assemble_team(self):
            while True:
                # Check if there are enough citizens to form a new team
                if self.r==0 or self.s==0 or (self.r + self.s < 4) or self.r<2 or (self.r>2 and self.s<2):
                    if self.r>2 and self.s==1: pass
                    else: # Not enough citizens to form another team
                        for _ in range(self.r):
                            self.rc_id+=1
                            self.r-=1
                            print(f'Regular Citizen {self.rc_id} is signing up')
                        for _ in range(self.s):
                            self.sc_id+=1
                            self.s-=1
                            print(f'Super Citizen {self.sc_id} is signing up')
                        break
                
                # Need at least 1 Super Citizen
                self.super_queue.acquire()  
                with self.lock:
                    self.s -= 1
                    super_count = 1
                    self.team_id += 1
                    self.sc_id += 1
                    team_id = self.team_id
                    print(f'Super Citizen {self.sc_id} is signing up')

                # Attempt to add a second Super Citizen
                if (self.r==2 and self.s>0) or self.super_queue.acquire(blocking=False):
                    with self.lock:
                        if self.s > 0:
                            self.s -= 1
                            self.sc_id += 1
                            super_count += 1
                            print(f'Super Citizen {self.sc_id} is signing up')
                        else:
                            self.regular_queue.release()  # Release if not used

                # Regular Citizens Sign-up
                regular_needed = 4 - super_count
                for _ in range(regular_needed):
                    self.regular_queue.acquire()
                    with self.lock:
                        self.r -= 1
                        self.rc_id += 1
                        print(f'Regular Citizen {self.rc_id} is signing up')
                        self.regular_queue.release()

                # Joining and sending team        
                with self.lock:
                    self.total_teams_sent += 1
                    self.unsent_rc = self.r
                    self.unsent_sc = self.s

                    temp_id = self.sc_id - super_count
                    for _ in range (super_count):
                        temp_id+=1
                        print(f'Super Citizen {temp_id} has joined team {team_id}')

                    temp_id = self.rc_id - regular_needed
                    for _ in range (regular_needed):
                        temp_id+=1
                        print(f'Regular Citizen {temp_id} has joined team {team_id}')
                    print(f'team {team_id} is ready and now launching to battle (sc: {super_count} | rc: {4 - super_count})\n')

    def run(self):
        # Citizen queueing simulation
        threads = []

        # Start a single thread for all regular citizens
        regular_citizens_thread = Thread(target=self.regular_citizen, daemon=True)
        regular_citizens_thread.start()
        threads.append(regular_citizens_thread)

        # Start a single thread for all super citizen
        super_citizen_thread = Thread(target=self.super_citizen, daemon=True)
        super_citizen_thread.start()
        threads.append(super_citizen_thread)

        # Start a single thread for assembling team
        assemble_team_thread = Thread(target=self.assemble_team)
        assemble_team_thread.start()
        threads.append(assemble_team_thread)

        # Wait for all threads to complete
        for t in threads:
            print(f"Joining")
            t.join()

        print(f"\nTotal teams sent: {self.total_teams_sent}")
        print(f"Unsent Regular Citizens: {self.unsent_rc}\nUnsent Super Citizens: {self.unsent_sc}")

if __name__ == "__main__":
    #UNCOMMENT FOR SUBMISSION
    # r = int(input("Input the total number of regular citizens: "))
    # s = int(input("Input the total number of super citizens: "))

    # if(r >= 0 and s >= 0):
    #     print("\n")
    #     hq = Helldivers(r, s)
    #     hq.run()
    
    hq = Helldivers(32, 12) 
    hq.run()

    print("\n-----------------END-----------------\n")