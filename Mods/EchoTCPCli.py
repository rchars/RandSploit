import ModInterface.ModInterface as modiface
import Option.Option as opt
import socket
import time



class Mod(modiface.ModInterface):
	def __init__(self):
		super().__init__('EchoTCP>')
		self.rport = opt.ValidatedOpt('RPORT', descr='Target port', validator=int)
		self.rhost = opt.DefaultOpt('RHOST', descr='Target host', required=True)
		# what about negative floats ??
		self.send_delay = opt.ValidatedOpt('SEND_DELAY', 3.5, 'Delay before next send', validator=float)
		self.timeout = opt.ValidatedOpt('TIMEOUT', 5.5, 'Timeout before disconnecting', validator=float)
		self.send_message = opt.DefaultOpt('PING_STR', 'Echo TCP', 'Message to send')

	def run(self):
		while True:
			try:
				s = socket.create_connection((self.rhost.value, self.rport.value), timeout=self.timeout.value)
				s.send(f'{send_message}\n'.encode())
				for buff in self.recv_till_sep(s):
					print(buff, end='')
			except OSError as e:
				print(e)
			try:
				s.close()
			except UnboundLocalError:
				pass
			time.sleep(send_delay)

	def recv_till_sep(self, s):
		end_recv = False
		seps = ('\n', '\r\n')
		while not end_recv:
			buff = s.recv(1024).decode()
			if buff[-1] in seps:
				end_recv = True
			yield buff
