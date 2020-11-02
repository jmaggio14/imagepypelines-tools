from .util import BaseCommThread, TCPServer, EventQueue
from functools import partial
from json import loads, dumps
from struct import pack, unpack
from typing import Tuple
import select
import threading


# __ Chatroom Object _________________________________________________________
class Chatroom(BaseCommThread):

    def __init__(self, app, host='0.0.0.0', port=9000):
        super().__init__()
        self.host = host
        self.port = port
        self.dashboard = app
        self.events = EventQueue()  # Class that queues events
        self.sessions = {} # List of all available tcp sessions (including host)
        self.msg_buff = {}

    def disconnect_client(self, c):
        print(f"Yeeting Pipe {self.sessions[c]['uuid']}")
        del self.msg_buff[self.sessions[c]['uuid']]
        c.close()
        del self.sessions[c]
        print("Sessions (CURRENT):   ", self.sessions)

    def disconnect_all(self):
        clients = [c for c in self.sessions if self.sessions[c] is not None]
        map(partial(Chatroom.disconnect_client, self.sessions), clients)
        for s in self.sessions.keys():  # Kill the Socket Server last
            s.close()

    @staticmethod
    def recvall(c, length):
        '''Convenience function to read large amounts of data (>4096 bytes)'''
        data = b''
        while len(data) < length:
            remaining = length - len(data)
            try:
                data += c.recv(min(remaining, 4096))
            except BlockingIOError as err:
                print(f"ERROR received when reading from socket{c}:\n{err}")
                break
        return data

    @staticmethod
    def write(c, msg):
        msg_b = msg.encode()
        length = pack('>Q', len(msg_b))
        c.sendall(length) # send length of the message as 64bit integer
        c.sendall(msg_b) # send the message itself

    def read(self, c):
        line = c.recv(8) # 8 bytes for 64bit integer
        if line == b'': # Case for a disconnecting Client socket
            return None
        length = unpack('>Q', line)[0]
        return self.recvall(c, length).decode().rstrip()

    def connect(self, c):
        c, a = c.accept()
        print(f"Connecting Pipe {a}")
        self.sessions[c] = {'addr': str(a[0]) + ':' + str(a[1]) , 'uuid': 'undefined', 'graph': 'undefined', 'status': []}

    def push(self, msg):
        ''' Function to be used outside of the Chatroom class '''
        self.events.add_task(msg)

    def parse_session_msg(self, c, msg):
        _msg = loads(msg)
        if _msg['type'] == 'graph':
            uuid = _msg['uuid']
            self.sessions[c]['uuid'] = uuid
            self.sessions[c]['graph'] = _msg
            self.msg_buff[uuid] = []
        elif _msg['type'] == 'status':
            if self.sessions[c] is not None and 'status' in self.sessions[c]:
                self.sessions[c]['status'].append(_msg)
            else:
                self.sessions[c]['status'] = [_msg]
            pass
        elif _msg['type'] == 'reset':
            pass
        elif _msg['type'] == 'block_error':
            pass
        elif _msg['type'] == 'delete':
            pass
        elif _msg['type'] == 'log':
            pass
        else:
            pass

        return msg

    def parse_dashboard_msgs(self, msg_list):
        # RH - definitely some debug (easter eggs?) printing going on here lol
        for msg in msg_list:
            print("_msg content is.....   ", msg)

            try:
                _msg = loads(msg)
            except:
                print("OOOOOOOF @ JSON BOIIIIII")

            print("Type of _msg is.....   ", type(_msg))
            uuid = _msg['uuid']
            print("Retrieved uuid is...   ", uuid)
            try:
                print("msg_buff is.......   ", self.msg_buff)
                self.msg_buff[uuid].append(msg)
            except KeyError:
                # TODO: Emit error message to client sender; Invalid Pipe ID
                pass

    def run(self):
        t = threading.current_thread()  # Grab current threading context
        # __ Dashboard Event Loop State Info _________________________________
        tcp = TCPServer()
        s = tcp.connect(self.host, self.port) # Grab server object (Chatroom host)
        sock = s.sock
        self.sessions[sock] = None  # Add host to sessions list
        print("\nSessions (INIT):   ", self.sessions)
        # __ Dashboard Event Loop Start ______________________________________
        while getattr(t, 'running', True):  # Run until signaled to DIE
            ready2read, ready2write, _ = select.select(self.sessions, self.sessions, [], 0.1)
            ready2read = [c for c in ready2read if c.fileno() != -1]
            ready2write = [c for c in ready2write if c.fileno() != -1]
            for c in ready2read:
                if c is sock:  # If there is a Pipeline requesting a connection
                    self.connect(c)
                    print("Sessions (CURRENT):   ", self.sessions)
                    continue
                # If we get to this point then a client has sent a message
                msg = self.read(c)
                if msg: # If they sent anything (even a blank return)
                    # Do something to the data (RH: WE WILL REFORMAT TO RETE.JS NODE-LINK HERE)
                    msg = self.parse_session_msg(c, msg)
                    self.dashboard.emit('pipeline-update', msg, broadcast=True)
                else: # If they sent nothing (which for TCP, happens when a client disconnects)
                    self.disconnect_client(c)
                    if c in ready2write:
                        ready2write.remove(c)

            # Now check if any scheduled task is ready to be run
            msgs = self.events.run_scheduled_tasks()  # Runs any scheduled task
            try:
                self.parse_dashboard_msgs(msgs)
            except:
                print('Unable to parse ', msgs)
                # do nothing
            # Finally check if there is anything waiting to be sent to anyone
            for c in ready2write:
                # Check if there are messages to be sent to connected clients
                if (c is not sock):
                    uuid = self.sessions[c]['uuid']
                    if (uuid in self.msg_buff) and self.msg_buff[uuid]:
                        while self.msg_buff[uuid]:
                            msg = self.msg_buff[uuid].pop(0)
                            self.write(c, msg)

        # __ Dashboard Event Loop Cleanup ____________________________________
        self.disconnect_all()
