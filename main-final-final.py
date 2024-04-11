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
threading.Lock() = mutex lock
'''

'''
SYNCHRONIZATION TECHNIQUE USED: SEMAPHORES
'''

class Helldivers:
    def __init__(self, r, s):
        self.r = r                  # Number of Regular Citizens
        self.s = s                  # Number of Super Citizens
        self.team_id = 0            # Team ID
        self.rc_id = 0              # Regular Citizens ID
        self.sc_id = 0              # Super Citizens ID
        self.regular_queue = Semaphore(1)   # Semaphore for Regular Citizens (Limit: 1)
        self.super_queue = Semaphore(1)     # Semaphore for Super Citizens (Limit: 1)
        self.lock = Lock()          # Mutex Lock
        self.super_count = 0        # Super Citizen count per team
        self.regular_count = 0      # Regular Citizen count per team
        self.total_teams_sent = 0   # Total Teams Sent
        self.unsent_rc = r          # Unsent Regular Citizens
        self.unsent_sc = s          # Unsent Super Citizens

    # Queue for Regular Citizens
    def regular_citizen(self):
        for _ in range(self.r):
            time.sleep(random.uniform(0.1, 0.5))  # to simulate queueing time
            self.regular_queue.release()

    # Queue for Super Citizens
    def super_citizen(self):
        for _ in range(self.s):
            time.sleep(random.uniform(0.1, 0.5))  # to simulate queueing time
            self.super_queue.release()

    def assemble_team(self):
        while True:
            self.super_count = 0    # Resets Super Citizens count to 0
            self.regular_count = 0  # Resets Regular Citizens count to 0

            # Check if there are enough citizens to form a new team
            ''' SATISFIES RULE #7 ''' 
            if self.r==0 or self.s==0 or (self.r + self.s < 4) or self.r<2 or (self.r>2 and self.s<2):
                if self.r>2 and self.s==1: pass # There is still 1 SC left and more than 2 RCs
                else: # Not enough citizens to form another team 
                    while self.r+self.s != 0:
                        if (random.uniform(0, 1) < 0.5): # to simulate first come first serve
                            if self.r > 0:
                                self.rc_id+=1
                                self.r-=1
                                print(f'Regular Citizen {self.rc_id} is signing up')
                        else:
                            if self.s > 0:
                                self.sc_id+=1
                                self.s-=1
                                print(f'Super Citizen {self.sc_id} is signing up')
                    break
            
            # TEAM ASSEMBLY #

            # First-come, first-serve basis
            ''' SATISFIES RULE #5 '''
            # Simulate who comes first
            if (random.uniform(0, 1) < 0.5):
                self.sc_signup()
                self.rc_signup()
            else:
                self.rc_signup()
                self.sc_signup()

            # Joining and sending team       
            ''' SATISFIES RULE #6''' 
            with self.lock:
                self.total_teams_sent += 1
                self.unsent_rc = self.r
                self.unsent_sc = self.s

                temp_id = self.sc_id - self.super_count
                for _ in range (self.super_count):
                    temp_id+=1
                    print(f'Super Citizen {temp_id} has joined team {self.team_id}')

                temp_id = self.rc_id - self.regular_count
                for _ in range (self.regular_count):
                    temp_id+=1
                    print(f'Regular Citizen {temp_id} has joined team {self.team_id}')

                print(f'team {self.team_id} is ready and now launching to battle (sc: {self.super_count} | rc: {self.regular_count})\n')

    # Super Citizen Sign up
    def sc_signup(self):
        # Need at least 1
        ''' SATISFIES RULE #1 & #2 '''
        self.super_queue.acquire()
        with self.lock:
            self.s -= 1
            self.super_count = 1
            self.team_id += 1
            self.sc_id += 1
            print(f'Super Citizen {self.sc_id} is signing up')

        # Attempt to add 2nd Super Citizen
        ''' SATISFIES RULE #2 & #3 '''
        if self.regular_count == 3: 
            self.super_queue.release()  # Release if not used
        elif self.regular_count == 2 or (self.r==2 and self.s>0) or self.super_queue.acquire(blocking=False):
            with self.lock:
                if self.s > 0:
                    self.s -= 1
                    self.sc_id += 1
                    self.super_count += 1
                    print(f'Super Citizen {self.sc_id} is signing up')
                else:
                    print("super_queue released\n")
                    self.super_queue.release()  # Release if not used

    # Regular Citizen Sign up
    def rc_signup(self):
        ''' SATISFIES RULE #1 & #4 '''
        if self.super_count == 0: # Regular Citizen came first
            if self.r>=2 and self.s==2:
                self.regular_count = 2
            elif self.r>2:
                self.regular_count = 3
            else:
                self.regular_count = 2
        else: # Regular Citizens fill up team
            self.regular_count = 4 - self.super_count 
        for _ in range(self.regular_count):
            self.regular_queue.acquire()
            with self.lock:
                self.r -= 1
                self.rc_id += 1
                print(f'Regular Citizen {self.rc_id} is signing up')
                self.regular_queue.release()

    def run(self):
        # Citizen queueing simulation
        threads = []

        # Thread for Regular Citizens
        regular_citizens_thread = Thread(target=self.regular_citizen, daemon=True)
        regular_citizens_thread.start()
        threads.append(regular_citizens_thread)

        # Thread for Super Citizens
        super_citizen_thread = Thread(target=self.super_citizen, daemon=True)
        super_citizen_thread.start()
        threads.append(super_citizen_thread)

        # Thread for Team Assembly
        assemble_team_thread = Thread(target=self.assemble_team)
        assemble_team_thread.start()
        threads.append(assemble_team_thread)

        # Joining of threads
        for t in threads:
            t.join()

        print(f"\nTotal teams sent: {self.total_teams_sent}")
        print(f"Unsent Regular Citizens: {self.unsent_rc}\nUnsent Super Citizens: {self.unsent_sc}")

if __name__ == "__main__":
    # # Ask for user input r, s
    # r = int(input("Input the total number of regular citizens: "))
    # s = int(input("Input the total number of super citizens: "))

    # # Checks if r & s are not negative
    # if(r >= 0 and s >= 0):
    #     print("\n")
    #     hq = Helldivers(r, s)
    #     hq.run()

    hq = Helldivers(15, 7)
    hq.run()

    print("\n-----------------END-----------------\n")