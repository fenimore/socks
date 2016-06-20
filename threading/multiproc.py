"""Threading example."""
import threading
from queue import Queue
import time



def example_job(worker):
    """Pretend to do work."""
    time.sleep(.5)
    with print_lock:
        print(threading.current_thread().name, worker)

def threader():
    while True:
        """Get worker from queue, and then finish talks"""
        worker = q.get()
        example_job(worker)
        q.task_done()


if __name__ == '__main__':
    """
    
    the threading object is a daemon, so they die when main dies
    """
    print_lock = threading.Lock()
    q = Queue()

    for x in range(10):
        t = threading.Thread(target=threader) # Target is all important
        t.daemon = True # lest they live on
        t.start()

    start_time = time.time()
    
    for worker in range(20):
        q.put(worker)

    q.join()

    print('Entire job took:', time.time() - start_time)
