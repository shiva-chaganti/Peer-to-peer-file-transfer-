
import socket
import struct
import threading
import traceback


class comm:
	
	"""
	Initialize the peer communication by setting providing peer_IP, 
	peer_PORT and peer socket object
	
	"""
	def __init__(self, host, port, sock = None):
		
		self.peer_host = host
		self.peer_port = int(port)
		self.peer_id = "%s:%d"%(self.peer_host, self.peer_port)
		print self.peer_id #
		
		if not sock:
			
			client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				client_sock.connect(self.peer_host, self.peer_port)
				print "Connected to {%s:%d}"%(self.peer_host, self.peer_port)
				
				#socket_data = self.client_sock.makefile('rw', 0)
			except:
				return False
		else:
			client_sock = sock
			
		self.socket_data = self.client_sock.makefile('rw',0)
	"""
	Sends message to the connected peer, if delivered returns True, else False
	
	"""
	
	def out_data(self, message_type, message):
		
		try:
			message_len = len(message)
			message_packet = struct.pack("!4sL%ds"% message_len, message_type, message_len, message)
			
			
			self.socket_data.write(message_packet)
			self.socket_data.flush()
			print "Message sent"
			
		except KeyboardInterrupt:
			raise
		except:
			traceback.print_exc()
			print "Message not sent"
			return False
		return True
		
	"""
	Receives message from the connected peer, retuns (message_type, message) on success
	
	"""
	def in_data(self):
		
		message_type = self.socket_data.read(4)
		
		try:
			
			if message_type:
				print "Message received"
				length = self.socket_data.read(4)
				message_len = int(struct.unpack("!L", length)[0])
				message_rcvd = ""
			
			while len(message_rcvd) != message_len:
				data = self.socket_data.read(min(2048, len(message_rcvd)))
				if not len(data):
					break
				message_rcvd += data
				
			if len(message_rcvd) != message_len:
				return (None, None)
			
		except KeyboardInterrupt:
			raise
		except:
			traceback.print_exc()
			return (None, None)
			
		return (message_type, message_rcvd)
		
	"""
	Closes the connection with the connected peer on calling
	
	"""	
	def close_conn():
		
		self.client_sock.close()
		self.client_sock = None
		self.socket_data = None
		

		
