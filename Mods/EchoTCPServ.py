import threading
import datetime
import modiface
import socket
import time


class Mod(modiface.ModInterface):
	def __init__(self):
		super().__init__('EchoTCPServ>')
		modiface.add_option(modiface.Option('LHOST', '', 'Hostname to listen on', required=True))
		modiface.add_option(modiface.CastOption('LPORT', None, 'Port to listen on', cast_to=int, required=True))
		modiface.add_option(modiface.CastOption('CLIENT_TIMEOUT', 10, 'Timeout before disconnecting', cast_to=float, required=False))
		modiface.add_option(modiface.CastOption('CLIENT_LIMIT', 1, 'Max number of clients that can connect', cast_to=float, required=False))

	def run(self):
		lhost = modiface.get_option_val('LHOST')
		lport = modiface.get_option_val('LPORT')
		client_limit = modiface.get_option_val('CLIENT_LIMIT')
		if not client_limit:
			client_limit = 1
		client_timeout = modiface.get_option_val('CLIENT_TIMEOUT')
		if not client_timeout:
			client_timeout = 10
		serv_sock = socket.create_server((lhost, lport))
		serv_sock.listen(client_limit)
		self.time_print(f'listening on {lhost}:{lport}')
		while True:
			try:
				client_sock, client_info = serv_sock.accept()
				client_sock.settimeout(client_timeout)
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
