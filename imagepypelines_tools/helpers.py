import socket, time, threading, logging
from collections import namedtuple


# __ Logger Initialization ___________________________________________________
# [JEFF] REPLACE THE DEFAULT LOGGER WITH YOUR FANCY ONE
logging.basicConfig(level=logging.DEBUG)


# __ Socket Functions ________________________________________________________
def sockspeak(msg):
    if type(msg) is str:
        msg = msg.encode()
    return msg

def normalspeak(msg):
    if type(msg) is bytes:
        msg = msg.decode()
    return msg.rstrip()

def create_non_blocking_udp_client(host, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #<-- UDP SOCKET
    c.setblocking(0)
    c.connect((host,port))
    return c

def create_non_blocking_udp_server(host, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # <-- UDP SOCKET
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # <-- Reuse addr
    c.bind((host,port))  # <-- bind socket server to host & port
    c.setblocking(0)
    return c

def create_non_blocking_tcp_client(host, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #<-- UDP SOCKET
    c.connect((host,port))
    c.setblocking(0)
    return c

def create_non_blocking_tcp_server(host, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # <-- UDP SOCKET
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # <-- Reuse addr
    c.setblocking(0)
    c.bind((host,port))  # <-- bind socket server to host & port
    c.listen(10)  # <-- max of 10 unaccepted connections before not accepting anymore
    return c


# __ Parent Thread Manager Class _____________________________________________
class BaseCommThread(threading.Thread):
    '''
    Parent Class to all thread manager classes.
    '''
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.daemon = True

    def __enter__(self):
        '''
        Starts the thread in its own context manager block.
        Note: If the running thread is meant to be run indefinitely it is not
              recommended to use it as a context manager as once you exit the
              context manager, the thread will safely shut down via the
              __exit__() method.
        '''
        self.run()

    def __exit__(self, exc_type, exc_value, traceback):
        '''
        Is called once the context leaves the manager, safely signals the
        running thread to shutdown.
        '''
        self.stop_thread()

    # ____ Run Function ______________________________________________________
    def run(self):
        '''
        This function is to be overloaded in the child class. If the thread is
        to be run indefinitely (as in not for a fixed duration), you MUST
        structure this function as follows:

        --[START]--------------------------------------------------------------
        self.t = threading.current_thread()  # Grab current threading context
        ...
        while getattr(self.t, 'running', True):
            ...
        ...
        --[END]--------------------------------------------------------------

        This is necessary as the classes stop_thread() method can safely shut
        down the running thread by changing self.running to False, thus
        invalidating the while loop's condition.
        '''
        pass

    # ____ Thread Killer _____________________________(Kills with kindness)___
    def stop_thread(self):
        '''
        This is a convenience function used to safely end the running thread.
        Note: This will only end the running thread if the run() function
              checks for the classes 'running' attribute (as demonstrated in
              the docstring of the run() function above).
              This only works if the running thread is not hanging, this will
              prevent the while loop from re-evaluating its condition
        '''
        logging.warning("Closing Thread " + self.name)
        self.running = False
        self.join()
        logging.warning(f"{self.name} has stopped")



# [JEFF] I am probably going to move this into a more generic core/ file,
#        any suggestions?
# __ Event/Method Queueing Class _____________________________________________
class EventQueue:
    '''
    This Class is meant to be a simple task scheduler that runs tasks in any
    of the following ways:
        * Immediately
        * After a delay (seconds)
        * After a delay & repeatedly every specified interval of time (seconds)
    '''
    ScheduledEvent = namedtuple('ScheduleEvent', ['event_time', 'task'])

    def __init__(self):
        self.events = []

    def run_scheduled_tasks(self):
        ''' Runs all tasks that are scheduled to run at the current time '''
        t = time.monotonic()
        while self.events and self.events[0].event_time <= time.monotonic():
            event = heappop(self.events)
            event.task()

    def add_task(self, event_time, task):
        'Helper function to schedule one-time tasks at specific time'
        heappush(self.events, EventQueue.ScheduledEvent(event_time, task))

    def call_later(self, delay, task):
        'Helper function to schedule one-time tasks after a given delay'
        self.add_task(time.monotonic() + delay, task)

    def call_periodic(self, delay, interval, task):
        'Helper function to schedule recurring tasks'
        def inner():
            task()
            self.call_later(interval, inner)
        self.call_later(delay, inner)
