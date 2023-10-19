import ModBuilder.ModBuilder as mb
import threading
import socket


class Mod(mb.ModIface):
	def __init__(self):
		self.lhost = mb.OptTemplate.CommonNet.LHOST
		self.lport = mb.OptTemplate.CommonNet.LPORT
		self.rhost = mb.OptTemplate.CommonNet.RHOST
		self.rport = mb.OptTemplate.CommonNet.RPORT
		self.client_limit = mb.OptTemplate.CommonNet.CLI_LIMIT

	def run(self):
		try:
			serv_sock = socket.create_server((self.lhost.value, self.lport.value))
			serv_sock.listen(self.client_limit.value)
			while True:
				cli_sock_1 = serv_sock.accept()[0]
				cli_sock_2 = socket.create_connection(
					(
						self.rhost.value,
						self.rport.value
					)
				)
				self.thread_handler(
					cli_sock_1,
					cli_sock_2
				)
		finally:
			serv_sock.close()

	def thread_handler(self, cli_sock_1, cli_sock_2):
		try:
			thread_1 = threading.Thread(target=self.swap_data, args=(cli_sock_1, cli_sock_2,), daemon=True)
			thread_2 = threading.Thread(target=self.swap_data, args=(cli_sock_2, cli_sock_1,), daemon=True)
			thread_1.start()
			thread_2.start()
			thread_1.join()
		finally:
			for sock in (cli_sock_1, cli_sock_2):
				try:
					sock.close()
				except OSError: pass

	def swap_data(self, src_sock, dest_sock):
		try:
			while True:
				data = src_sock.recv(1024)
				print(data)
				if data == b'': break
				dest_sock.send(data)
		except(Exception, BrokenPipeError, OSError, TimeoutError) as reason:
			print(reason)
		else: print('Normal exit')
