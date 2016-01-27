

import threading
from Tkinter import *

from Peer_str import Peer_str

class User_Interface(Frame):
	
	def __init__(self, peer_next, max_peers = 2, server_port = 8989, master = None):
		
		Frame.__init__(self, master)
		
		self.grid()
		self.UI_Elements()
		self.master.title("P2P File Sharing Application")
		
		self.server_port = str(server_port)
		self.peer = Peer_str(max_peers, server_port)
		self.host, self.port = peer_next.split(':')
		self.peer.add_peer(self.host, self.port)
		
		p_file = self.peer.peer_files()
		if self.filelist.size() > 0:
			self.filelist.delete(0, self.filelist.size() - 1)
		for k,v in p_file.items():
			self.filelist.insert(END, k)
		
		
		t = threading.Thread( target = self.peer.listen_incoming_conn, args = [] )
		t.start()
		
		self.peer.peer_status()
			
		"""
		s = peer.create_socket()
		peer.send_message_to_peer(host, int(port), "GENL","HAII")
		
		peer.listen_incoming_conn()
		"""
		
			
	#def get_file_list(self):
		
		#selection = self.peerlist.curselection()
		
	def current_peer_list(self):
		own_id = "%s:%s"%(self.peer.peer_host, self.server_port)
		
		if self.peerlist.size() > 0:
			self.peerlist.delete(0, self.peerlist.size() - 1)
		self.peerlist.insert(END, own_id)
		for host, port in self.peer.peer_info.items():
			p = '%s:%s'%(host, port)
			self.peerlist.insert(END, p)
		
			
	def refresh(self):
		self.current_peer_list()
	
	def UI_Elements(self):
			
		frame_files = Frame(self)
		frame_peers = Frame(self)
		frame_search = Frame(self)
		frame_addfile = Frame(self)
		frame_refresh = Frame(self)
			
		frame_files.grid(row = 0, column = 0, sticky = N+S)
		frame_peers.grid(row = 1, column = 1, sticky = N+S)
		
		frame_search.grid(row = 4)
		frame_addfile.grid(row = 3)
		frame_refresh.grid(row = 3, column = 1)
		
		Label(frame_files, text = "Files").grid()
		Label(frame_peers, text = "Peer List").grid()
		
		frame_filelist = Frame(frame_files)
		frame_filelist.grid(row = 1, column = 0)
		scroll_filelist = Scrollbar(frame_filelist, orient = VERTICAL)
		scroll_filelist.grid(row = 0, column = 1, sticky = N+S)
		self.filelist = Listbox(frame_filelist, height = 5, yscrollcommand = scroll_filelist.set)
		self.filelist.grid(row = 0, column = 0, sticky = N+S)
		scroll_filelist["command"] = self.filelist.yview
		
		self.download_button = Button(frame_files, text = "Download", command = self.download)
		self.download_button.grid(row = 1, column = 2)
		
		#self.showfile = Entry(frame_addfile, width = 25)
		self.showfile_button = Button(frame_files, text = "File Info", command = self.get_file_list)
		#self.showfile.grid(row = 0, column = 0)
		self.showfile_button.grid(row = 1, column = 3)
		"""
		self.search = Entry(frame_search, width = 25)
		self.search_button = Button(frame_search, text = "Refresh", command = self.refresh)
		self.search.grid(row = 0, column = 0)
		self.search_button.grid(row = 0, column = 1)
		"""
		frame_peerlist = Frame(frame_peers)
		frame_peerlist.grid(row = 1, column = 0)
		scroll_peerlist = Scrollbar( frame_peerlist, orient=VERTICAL )
		scroll_peerlist.grid(row = 0, column =1 , sticky=N+S)
		self.peerlist = Listbox(frame_peerlist, height = 5, yscrollcommand = scroll_peerlist.set)
		self.peerlist.grid(row = 0, column = 0, sticky = E+W)
		scroll_peerlist["command"] = self.peerlist.yview	
		
		self.refresh_button = Button(frame_refresh, text = "Refresh", command = self.refresh)
		self.refresh_button.grid(row=0, column=1)
	
	

	
	
	def get_file_list(self):
		selection = self.peerlist.curselection()
		if len(selection) == 1:
			peer_id = self.peerlist.get(selection[0])
			host, port = peer_id.split(':')
			self.peer.send_message_to_peer(host, int(port), 'FLIST','')
				
	def download(self):
		selection = self.filelist.curselection()
		if len(selection) == 1:
			file_sel = self.filelist.get(selection[0])
			if file_sel in self.peer.file_info.keys():
				source_addr = self.peer.file_info[file_sel]
				host, port = source_addr.split(':')
				self.peer.send_message_to_peer(host, int(port), 'FGET', file_sel)
		
	
def main():
	server_port = 8989
	#response = raw_input("Enter the IP of initial peer to be connected:")
	#peer_ip = str(response)
	#peer_id = '%s:%d'%(peer_ip, server_port)
	print peer_id
	peer_id = "#.#.#.#:%s"%(8989)
	max_peers = 2
	app = User_Interface(peer_id, max_peers = max_peers, server_port = server_port)
	app.mainloop()
	
if __name__ == '__main__':
	main()
