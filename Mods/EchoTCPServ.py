import ModInterface.ModInterface as mod_iface
import Option.Option as opt
import threading
import datetime
import socket
import time


# This module is old
class Mod(mod_iface.ModInterface):
	def __init__(self):
		super().__init__(mod_descr='TCP echo server')
		self.lhost = opt.DefaultOpt('LHOST', descr='Hostname to listen on')
		self.lport = opt.ValidatedOpt('LPORT', descr='Port to listen on', validator=int)
		self.client_timeout = opt.ValidatedOpt('CLIENT_TIMEOUT', value=10, descr='Timeout before disconnecting', validator=float, required=False)
		self.client_limit = opt.ValidatedOpt('CLIENT_LIMIT', 1, descr='Max number of clients that can connect', validator=int, required=False)

	def run(self):
		if not self.client_limit.value:
			self.client_limit.value = 1
		if not self.client_timeout.value:
			self.client_timeout.value = 10
		serv_sock = socket.create_server((self.lhost.value, self.lport.value))
		serv_sock.listen(self.client_limit.value)
		self.time_print(f'listening on {self.lhost.value}:{self.lport.value}')
		while True:
			try:
				client_sock, client_info = serv_sock.accept()
				client_sock.settimeout(self.client_timeout.value)
				self.time_print(f'{client_info[0]}:{client_info[1]} (connected)')
				threading.Thread(target=self.handle_client, args=(client_sock, client_info)).run()
			except ConnectionError as conn_err:
				self.time_print(conn_err)
			except threading.ThreadError as thread_err:
				self.time_print(thread_err)

	def handle_client(self, client_sock, client_info):
		try:
			end_thread = False
			while not end_thread:
				data = ''
				buff = ''
				eol_index = None
				end_loop = False
				while not end_loop:
					if not buff:
						buff = client_sock.recv(1024).decode()
					if buff == '':
						end_thread = True
						break
					eol_index = buff.find('\n')
					if eol_index == -1:
						eol_index = 1023
					else:
						end_loop = True
					data += buff[:eol_index + 1]
					buff = buff[eol_index + 1:]
				if data:
					self.time_print(f'{client_info[0]}:{client_info[1]}>{data}', eol='')
					client_sock.send(b'EchoTCP:' + data.encode())
		except socket.timeout:
			self.time_print(f'{client_info[0]}:{client_info[1]} disconnected (timeout)')
			client_sock.close()
		else:
			self.time_print(f'{client_info[0]}:{client_info[1]} disconnected')

	def time_print(self, data, eol='\n'):
		current_time = datetime.datetime.now()
		formatted_current_time = current_time.strftime('%H:%M:%S')
		print(f'[{formatted_current_time}]{data}', end=eol)
