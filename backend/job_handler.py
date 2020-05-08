import time 
import threading
from queue import Queue

# Statics
RUN_TIMEOUT = 5

# Global Job Queue
job_queue = Queue()

# Maintain a dictionary of email to thread
job_thread_dict = dict()

# Class Definitions
class Job():
    profile = None
    state = ''

    def __init__(self, profile, state):
        self.profile = profile
        self.state = state

def add_job_to_job_queue(profile):
    global job_queue
    job_queue.put(profile)

def remove_job_from_job_queue(profile):
    global job_queue
    
    # stop thread, or cancel before its run? 

def run_jobs(): 
    global job_queue
    global job_thread_dict

    while True:
        if job_queue.empty() is False: 
            next_profile = job_queue.get()
            job_thread = threading.Thread(target=thread_func_stub, args=(next_profile))
            job_thread_dict[next_profile.gmail] = job_thread

        time.sleep(RUN_TIMEOUT)


def thread_func_stub(some_profile):
    print(some_profile.email)
    print("threading works")
    time.sleep(100)
    