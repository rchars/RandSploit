import ModInterface.ModInterface as mod_iface
import ModBuilder.ModBuilder as mb
import threading
import traceback
import datetime
import socket
import time


# This module is old
class Mod(mod_iface.ModInterface):
	def __init__(self):
		super().__init__(mod_descr='TCP echo server')
		self.lhost = mb.Opt.DefaultOpt('LHOST', value='localhost', descr='Hostname to listen on')
		self.lport = mb.Opt.ValidatedOpt('LPORT', value=9999, descr='Port to listen on', validator=int)
		self.client_timeout = mb.Opt.ValidatedOpt('CLIENT_TIMEOUT', value=3, descr='Timeout before disconnecting', validator=float, required=False)
		self.client_limit = mb.Opt.ValidatedOpt('CLIENT_LIMIT', 3, descr='Max number of clients that can connect', validator=int, required=False)

	def run(self):
		if not self.client_limit.value:
			self.client_limit.value = 1
		if not self.client_timeout.value:
			self.client_timeout.value = 5
		serv_sock = socket.create_server((self.lhost.value, self.lport.value), reuse_port=True)
		self.time_print(f'listening on {self.lhost.value}:{self.lport.value}')
		while True:
			try:
				client_sock, client_info = serv_sock.accept()
				client_sock.settimeout(self.client_timeout.value)
				self.time_print(f'{client_info[0]}:{client_info[1]} => Connected')
				handle_client = threading.Thread(target=self.handle_client, args=(client_sock, client_info))
				handle_client.daemon = True
				handle_client.start()
			except threading.ThreadError as thread_err:
				self.time_print(thread_err)

	def handle_client(self, client_sock, client_info):
		handle_recv = mb.Util.Net.RecvLines(client_sock)
		for line in handle_recv.recv_till_dead():
			self.time_print(f'{client_info[0]}:{client_info[1]}>{line}', eol='')
			client_sock.send('EchoTCP:'.encode() + line.encode())
		self.time_print(f'{client_info[0]}:{client_info[1]}>{handle_recv.reminder}')
		self.time_print(f'{client_info[0]}:{client_info[1]} => disconnected => {handle_recv.death_reason}')

	def time_print(self, data, eol='\n'):
		current_time = datetime.datetime.now()
		formatted_current_time = current_time.strftime('%H:%M:%S')
		print(f'[{formatted_current_time}]{data}', end=eol)
