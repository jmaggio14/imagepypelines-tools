# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018 - 2020 Jeff Maggio, Jai Mehra, Ryan Hartzell
import inspect
import collections
import time
import socket
import threading
from heapq import heappush, heappop
from struct import pack, unpack

MAX_UNACCEPTED_CONNECTIONS = 10


################################################################################
#                                 Socket Helpers
################################################################################
class BaseTCP(object):
    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #<-- TCP SOCKET

    # --------------------------------------------------------------------------
    def disconnect(self):
        self._s.close()

    # --------------------------------------------------------------------------
    @staticmethod
    def recvall(c, length):
        '''Convenience function to read large amounts of data (>4096 bytes)'''
        data = b''
        while len(data) < length:
            remaining = length - len(data)
            data += c.recv(min(remaining, 4096))
        return data

    # --------------------------------------------------------------------------
    def write(self, msg):
        msg_b = msg.encode()
        length = pack('>Q', len(msg_b))
        self._s.sendall(length) # send length of the message as 64bit integer
        self._s.sendall(msg_b) # send the message itself

    # --------------------------------------------------------------------------
    def read(self):
        """
        """
        line = self._s.recv(8) # 8 bytes for 64bit integer
        if line == b'':
            return None
        length = unpack('>Q', line)[0]
        return self.recvall(self._s, length)

    # --------------------------------------------------------------------------
    @property
    def sock(self):
        """:obj:`socket.Socket`: socket for this TCP connection"""
        return self._s

    # --------------------------------------------------------------------------
    @property
    def host(self):
        """str: ip address for this socket, or None if not connected"""
        # if the socket isn't connected, just return None
        try:
            return self._s.getsockname()[0]
        except OSError:
            return None

    # --------------------------------------------------------------------------
    @property
    def port(self):
        """int: port for this socket, or None if not connected"""
        # if the socket isn't connected, just return None
        try:
            return self._s.getsockname()[1]
        except OSError:
            return None

################################################################################
class TCPClient(BaseTCP):
    # --------------------------------------------------------------------------
    def connect(self, host, port):
        """connects and binds the socket to the given host and port

        Args:
            host(str): ip address to connect to
            port(int): port to connect to
        """
        self._s.connect( (host,port) )  # <-- connect socket server to host & port
        self._s.setblocking(0)

        return self


################################################################################
class TCPServer(BaseTCP):
    """
    NOTE:
        TCP Server has no explicit implementation of accepting/closing client
        connections. That is up to the implementation as needed. Socket object
        can be retrieved via:
            self.sock
    """
    def __init__(self):
        super().__init__()
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # --------------------------------------------------------------------------
    def connect(self, host, port=0):
        """connects and binds the socket to the given host and port

        Args:
            host(str): ip address to host on
            port(int): port to host on, leave as 0 for the OS to choose
                a port for you
        """
        print(f"TCPServer started at {host}:{port}")
        self._s.bind( (host,port) )  # <-- bind socket server to host & port
        self._s.setblocking(0)
        self._s.listen(MAX_UNACCEPTED_CONNECTIONS)  # <-- max of 10 unaccepted connections before not accepting anymore

        return self

################################################################################
#                                 Thread Helpers
################################################################################
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
        # RH - put these messages back in as they're useful for debug. Would be
        #      good to move logger and other utilities from imagepypelines into
        #      iptools for consistency (and so we can use stuff like the logger)
        print(f"\n\nClosing {self.name} thread...")
        self.running = False
        self.join()
        print(f"{self.name} has stopped.")


################################################################################
#                                 Event Helpers
################################################################################
class EventQueue:
    '''
    This Class is meant to be a simple task scheduler that runs tasks in any
    of the following ways:
        * Immediately
        * After a delay (seconds)
        * After a delay & repeatedly every specified interval of time (seconds)
    '''
    ScheduledEvent = collections.namedtuple('ScheduleEvent',
                                            ['event_time', 'task'])

    def __init__(self):
        self.events = []

    @staticmethod
    def funcify(obj):
        if callable(obj):
            return obj
        else:
            return lambda: obj

    def run_scheduled_tasks(self):
        ''' Runs all tasks that are scheduled to run at the current time '''
        t = time.monotonic()
        task_returns = []
        while self.events and self.events[0].event_time <= time.monotonic():
            event = heappop(self.events)
            task_return = event.task()
            task_returns.append(task_return)
        return [t for t in task_returns if t is not None]

    def add_task(self, task, event_time=None):
        print(f"task = {task}")
        task = self.funcify(task)
        'Helper function to schedule one-time tasks at specific time'
        if event_time is None:
            event_time = time.monotonic()
        heappush(self.events, EventQueue.ScheduledEvent(event_time, task))

    def call_later(self, task, delay):
        task = self.funcify(task)
        'Helper function to schedule one-time tasks after a given delay'
        self.add_task(task, time.monotonic() + delay)

    def call_periodic(self, task, delay, interval):
        task = self.funcify(task)
        'Helper function to schedule recurring tasks'
        def inner():
            self.call_later(inner, interval)
            return task()
        self.call_later(inner, delay)
