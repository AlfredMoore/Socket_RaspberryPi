import socket
import time
import sys
import json
import pickle
from typing import List, Tuple, Dict


class SocketInterface_PC:

    def __init__(self, SERVER_IP="192.168.31.52", SERVER_PORT=50000) -> None:
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        # # IP address of Rasberry Pi
        # SERVER_IP = "192.168.31.87"
        # SERVER_PORT = 8888
    
        print("Starting socket: TCP...")
        self.server_addr = (self.SERVER_IP, self.SERVER_PORT)
        # socket.AF_INET: IP protocol       socket.SOCK_STREAM: TCP Comm
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        while True:
            try:
                print("Connecting to server @ %s:%d..." %(self.SERVER_IP, self.SERVER_PORT))
                self.socket_tcp.connect(self.server_addr)
                break
            except Exception:
                print("Can't connect to server, try it latter!")
                time.sleep(1)
                continue
        
        data_recv = self.socket_tcp.recv(512)       # buffer lenth: max 512 Bytes each time
        if len(data_recv)>0:
            dict_recv = json.loads(data_recv)
            print("Receive:", dict_recv)           # receive "Welcome to Pupper Rpi TCP server!"


    def subscriber_env(self) -> Dict:

        data = self.socket_tcp.recv(512)
        if len(data)>0:
            # dict
            dict_recv = json.loads(data)

            ### TODO feed pickle_recv to the RL Model ##########
            # print("State of the robot: ticks\n", dict_recv)   # current state of robot
            ##############################################

            return dict_recv


    def publisher_cmd(self, command: Dict):
        try:

            # command = {"servo_degree": np.array, "info": Dict}

            msg_cmd = json.dumps(command)
            self.socket_tcp.send(bytes(msg_cmd.encode('utf-8')))
            print("published...")

        except Exception:
            self.socket_tcp.close()
            self.socket_tcp=None
            print("publisher error")
            sys.exit(1)


    def __del__(self):
        self.socket_tcp.close()
        print("Terminate PC Socket Connection!")


if __name__ == "__main__":
    
    # Establish connection
    socket_PC = SocketInterface_PC()
    next_action = 1
    next_state = 0
    action = None
    
    # action
    # 1. send a cmd that indicates what's next
    cmd = {"next":next_action, "action": None, "info": None, "message": None}
    socket_PC.publisher_cmd( command=cmd )
    
    # 2. send action or receive state
    cmd = {"next": None, "action": action, "info": None, "message": None}
    socket_PC.publisher_cmd( command=cmd )
    
    
    # # state
    # # 1. send a cmd that indicates what's next
    # cmd = {"next":next_state, "action": None, "info": None, "message": None}
    # socket_PC.publisher_cmd( command=cmd )
    
    # # 2. send action or receive state
    # msg = socket_PC.subscriber_env()
    # state = msg["imu_data"]

