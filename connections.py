import socket
import threading


REC_BUFFER_SIZE = 2048


class ServerConnection:
    '''
    initiate
    '''
    def __init__(self,port,threads):
        self.host    = ''
        self.port    = port
        self.threads = threads        
    
    def open_socket_with_TCP(self): 
        try: 
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.server.bind((self.host,self.port)) 
            self.server.listen(self.threads) 
        except socket.error, (value,message): 
            if self.server: 
                self.server.close() 
            print "Could not open socket: " + message 
            sys.exit(1) 
    
    def open_socket_with_UDP(self): 
        try: 
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind((self.host,self.port)) 
            self.server.listen(5) 
        except socket.error, (value,message): 
            if self.server: 
                self.server.close() 
            print "Could not open socket: " + message 
            sys.exit(1) 
            
   
    '''
    inspect the ip address is ipv4 or not
    '''
    def is_valid_ipv4_address(address):
        try:
            addr= socket.inet_pton(socket.AF_INET, address)
        except AttributeError: # no inet_pton here, sorry
            try:
                addr= socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error: # not a valid address
            return False
        return True
    
    '''
    inspect the ip address is ipv6 or not
    '''
    def is_valid_ipv6_address(address):
        try:
            addr= socket.inet_pton(socket.AF_INET6, address)
        except socket.error: # not a valid address
            return False
        return True
    
    def run(self):
        self.open_socket_with_TCP()
        while True:
            c = ClientConnection(self.server.accept())
            print c.client,c.addr
            c.start()
    
    
    
class ClientConnection(threading.Thread):
    def __init__(self,(client,addr)):
        threading.Thread.__init__(self)
        self.client = client
        self.addr   = addr
        self.size   = REC_BUFFER_SIZE
    
    def run(self):
        while True:
            rec_data = self.client.recv(self.size)
            print 'rec:',rec_data
            if not rec_data: break
        print 'over'
        self.client.close()