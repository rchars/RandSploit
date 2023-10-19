import ModInterface.ModInterface as modiface
import ModBuilder.ModBuilder as mb
import Option.Option as opt
import socket
import time


class Mod(modiface.ModInterface):
	def __init__(self):
		super().__init__('EchoTCP>')
		self.rport = opt.ValidatedOpt('RPORT', value=9999, descr='Target port', required=True, validator=int)
		self.rhost = opt.DefaultOpt('RHOST', value='localhost', descr='Target host', required=True)
		self.send_delay = opt.ValidatedOpt('SEND_DELAY', 3.5, 'Delay before next send', required=True, validator=float)
		self.timeout = opt.ValidatedOpt('TIMEOUT', 5.5, 'Timeout before disconnecting', required=True, validator=float)
		self.send_message = opt.DefaultOpt('PING_STR', 'Echo TCP', 'Message to send', required=False)

	def run(self):
		while True:
			s = socket.create_connection((self.rhost.value, self.rport.value), timeout=self.timeout.value)
			s.send(f'{self.send_message.value}\n'.encode())
			handle_recv = mb.Util.Net.RecvLines(s)
			for line in handle_recv.recv_till_dead():
				print(line, end='')
			if handle_recv.reminder:
				print(handle_recv.reminder)
			if handle_recv.death_reason:
				print(handle_recv.death_reason)
			time.sleep(self.send_delay.value)
