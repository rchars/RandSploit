import ModInterface.ModInterface as modiface
import Option.Option as opt
import socket
import time


class Mod(modiface.ModInterface):
	def __init__(self):
		super().__init__('EchoTCP>')
		self.rport = opt.ValidatedOpt('RPORT', descr='Target port', required=True, validator=int)
		self.rhost = opt.DefaultOpt('RHOST', descr='Target host', required=True)
		self.send_delay = opt.ValidatedOpt('SEND_DELAY', 3.5, 'Delay before next send', required=True, validator=float)
		self.timeout = opt.ValidatedOpt('TIMEOUT', 5.5, 'Timeout before disconnecting', required=True, validator=float)
		self.send_message = opt.DefaultOpt('PING_STR', 'Echo TCP', 'Message to send', required=False)

	def run(self):
		while True:
			try:
				s = socket.create_connection((self.rhost.value, self.rport.value), timeout=self.timeout.value)
				s.send(f'{self.send_message.value}\n'.encode())
				for buff in self.recv_till_sep(s):
					print(buff, end='')
			except OSError as e:
				print(e)
			try:
				s.close()
			except UnboundLocalError:
				pass
			time.sleep(self.send_delay.value)

	def recv_till_sep(self, s):
		end_recv = False
		seps = ('\n', '\r\n')
		while not end_recv:
			buff = s.recv(1024).decode()
			if buff[-1] in seps:
				end_recv = True
			yield buff
