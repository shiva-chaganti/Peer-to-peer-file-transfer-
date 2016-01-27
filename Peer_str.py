

import socket
import threading
import traceback
import time
from os import listdir
from os.path import isfile, join
from comm import comm



class Peer_str:
	
	
	"""
	This initializes a peer with the below properties, such as the listening port, maximum peers it can
	connect with
	
	"""
	def __init__(self, max_peers, server_port, peer_id = None, peer_host = None, peer_next = None):
		
		self.max_peers = max_peers
		self.peer_port = server_port 
		
		"""
		if peer_host:
			self.peer_host = peer_host
		else:
			self.peer_host = socket.gethostbyname(socket.gethostname())
		"""
		self.peer_host = "10.226.43.247"
		print "Peer_Host ---> %s"%(self.peer_host)
		self.peer_id = "%s:%s" % (self.peer_host, self.peer_port)
		self.peer_next = peer_next
		print peer_next
		self.peer_info = {}
		self.p_lock = threading.Lock()
		#self.message_handlers = {'FGET':peer_file_get}
		self.shutdown = False
		self.file_info = {}
		
	def add_peer(self, host, port, peer_next = None):
		
		pid = '%s:%s'%(host, port)
		
			
		if  pid not in self.peer_info:
			self.peer_info[host] = port
			print "Peer info added"
			return True
		else:
			return False
			
	def peer_files(self):
		
		
		path = path = "/home/tej/Documents/Java Files"
		fl = [f for f in listdir(path) if isfile(join(path, f))]
		for files in fl:
			self.file_info[files] = self.peer_id
		return self.file_info
	#def file_list_handler(self):
		
	
	def handle_incoming_peer_message(self, client_sock):
		
		print "Peer {%s:%d} connected to %s"%(self.peer_host, self.peer_port, client_sock.getpeername())
		
		host, port = client_sock.getpeername()
		#print "Incoming PING from {%s:%d}"%(host, port)
		try:
			comm_peer = comm(host, port, client_sock)
			message_type, message = comm_peer.in_data()
			
			if message_type:
				message_type = message_type.upper()
			print "Message received:", message_type
			
			"""
			Stores the local file list into dictionary with peer_id as reference to every file
			"""
			if message_type == 'FLST':
				send_message_to_peer(host, port, 'FLRS', self.file_info)
			elif message_type == 'FLRS':
				temp = message.copy()
				temp.update(self.file_info)
				self.file_info = temp
				
			elif message_type == 'PLST':
				send_message_to_peer(host, port, 'PLST', self.peer_info)
			elif message_type == 'PLRS':
				for peer_id in message:
					if peer_id not in self.peer_info:
						self.peer_info.append(peer_id)
				
			elif message_type == 'FGET':
				if message in self.file_info.keys():
					try:
						fd = file(message, 'r')
						f_data = ''
						start_time = time.time()
						while True:
							data = fd.read(2048)
							if not len(data):
								break
							f_data += data
						fd.close()
					except:
						print "Error encountered downloading file"
						return
				send_message_to_peer(host, port, 'FRES', f_data)
				end_time = time.time()
				download_time = start_time - end_time 
				print download_time
				
				
			elif message_type == 'FRES':
				
				path = "/home/tej/Documents/Java Files"
				fl = [f for f in listdir(path) if isfile(join(path, f))]
				for files in fl:
					fd = open(files, 'rb')
					fd.seek(0,2)
					size = fd.tell()
					if size is None:
						target_file = files
				with open("/home/tej/Documents/Java Files/" + target_file) as tf:
					tf.write(message)
				
				
				
			
			
			if message_type not in self.message_handlers:
				print "Invalid message --> [%s:%s]"%(message_type, message)
			else:
				print "Responding to the message --> [%s:%s]"%(message_type, message)
				self.massage_handlers[message_type] = message
			
		
		except KeyboardInterrupt:
			raise
		except:
			traceback.print_exc()
			
		com.close_conn()
		
	"""
	Sends message to the connected peer over the TCP socket
	
	"""
	def send_message_to_peer(self, host, port, message_type, message):
		
		counter = 0
		total_recvd_message = []
		while counter != 1:
			try:
				print "Trying to connect to {%s:%d}"%(host, port)
				comm_peer = comm(host, port)
				print "Establishing communication with {%s:%d}"%(host, port)
				comm_peer.out_data(message_type, message)
				print "Message sent to {%s:%d}"%(host, port)
				recvd_message = comm_peer.in_data()
				while(recvd_message != (None, None)):
					total_recvd_message.append(recvd_message)
				print "Reply from {%s:%d} ---> %s"%(host, port, total_recvd_message)
				comm_peer.close_conn()
				break
			except KeyboardInterrupt:
				raise
			except:
				counter += 1
				print "No response from connected peer {%s:%d} --->%s [%d]"%(host, port, message_type, counter)
		
			
		return total_recvd_message
		
	
	def peer_status(self):
		
		not_alive = []
		for host, port in self.peer_info.items():
			isalive = False
			
			try:
				comm_peer = comm(host, port)
				comm_peer.out_data('PING','')
				isalive = True
			except:
				not_alive.append(host)
			if isalive:
				comm_peer.close_conn()
			
		self.p_lock.acquire()
		try:
			for offline_peers in not_alive:
				if self.peer_info[offline_peers]:
					del self.peer_info[offline_peers]
		finally:
			self.p_lock.release()	
	
	def create_socket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print self.peer_port
		s.bind((self.peer_host, self.peer_port))
		s.listen(5)
		#s.settimeout(1)
		
		return s
	
	
	
	"""
	Prepares a socket for the peer to handle communication and also continously listens for the incoming
	connection requests
	
	"""
	
	def listen_incoming_conn(self):
		
			
		print "Peer initialised :{%s:%d}"%(self.peer_host, self.peer_port) 
		
		s = self.create_socket()
		h,p = s.getsockname()
		print "Socket Created:{%s:%d}"%(h, p)
		while not self.shutdown:
			try:
				client_sock, client_addr = s.accept()
				print "Client Address", client_addr
				s.settimeout(None)
				s.listen(5)
				t = threading.Thread(target = self.handle_incoming_peer_message, args = [client_sock])
				t.start()
				
			except KeyboardInterrupt:
				print "Terminating the peer {%s:%d} connection"%(self.peer_host, self.peer_port)
				self.shutdown = True
			except:
				continue
				
		s.close()
		
	
		
