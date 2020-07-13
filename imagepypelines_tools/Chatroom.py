from imagepypelines.core.util import BaseCommThread, TCPServer, EventQueue
from functools import partial
from struct import pack, unpack
import select


# __ Chatroom Object _________________________________________________________
class DashboardChatroom(BaseCommThread):

    def __init__(self, host, port, socketio):
        super().__init__()
        self.host = host
        self.port = port
        self.dashboard = socketio

    @staticmethod
    def disconnect_client(sessions, c):
        c.close()
        del sessions[c]

    @staticmethod
    def disconnect_all(sessions):
        clients = [c for c in sessions if sessions[c] is not None]
        map(partial(DashboardThread.disconnect_client, sessions), clients)
        for s in sessions.keys():  # Kill the Socket Server last
            s.close()

    @staticmethod
    def recvall(c, length):
        '''Convenience function to read large amounts of data (>4096 bytes)'''
        data = b''
        while len(data) < length:
            remaining = length - len(data)
            data += c.recv(min(remaining, 4096))
        return data

    @staticmethod
    def write(c, msg):
        msg_b = msg.encode()
        length = pack('>Q', len(msg_b))
        c.sendall(length) # send length of the message as 64bit integer
        c.sendall(msg_b) # send the message itself

    @staticmethod
    def read(c):
        line = c.recv(8) # 8 bytes for 64bit integer
        length, _ = unpack('>Q', line)
        return recvall(c, length).decode().rstrip()

    def connect(self, c, sessions):
        c, a = c.accept()
        print(f"Connecting Pipe {a}")
        session[c] = a

    def run(self):
        t = threading.current_thread()  # Grab current threading context
        # __ Dashboard Event Loop State Info _________________________________
        s = TCPServer.connect(self.host, self.port)  # Grab server object (Chatroom host)
        sessions = {}   # List of all available tcp sessions (including host)
        # events = EventQueue()  # Class that queues events
        sessions[s] = None  # Add host to sessions list
        # __ Dashboard Event Loop Start ______________________________________
        while getattr(t, 'running', True):  # Run until signaled to DIE
            ready2read, _, _ = select.select(sessions, [], [], 0.1)
            for c in ready2read:
                if c is s:  # If there is a Pipeline requesting a connection
                    self.connect(c, sessions)
                    continue
                # If we get to this point then a client has sent a message
                msg = self.read(c)
                if msg: # If they sent anything (even a blank return)
                    # Do something to the data
                    print(msg)
                    self.dashboard.emit('pipeline-update', msg, broadcast=True)
                else: # If they sent nothing (which for TCP, happens when a client disconnects)
                    self.disconnect_client(c, sessions)
            # Now check if any scheduled task is ready to be run
            # events.run_scheduled_tasks() # Runs any scheduled task

        # __ Dashboard Event Loop Cleanup ____________________________________
        self.disconnect_all(sessions)
