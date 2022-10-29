import modiface
import socket
import time



class Mod(modiface.ModInterface):
	def __init__(self):
		super().__init__(prompt='EchoTCP>')
		modiface.add_option(modiface.Option('RHOST', '', 'Target host', required=True))
		modiface.add_option(modiface.CastOption('RPORT', '', 'Target port', int))
		modiface.add_option(modiface.CastOption('SEND_DELAY', 3.5, 'Delay before next send', float))
		modiface.add_option(modiface.CastOption('TIMEOUT', 5.5, 'Timeout before disconnecting', float))
		modiface.add_option(modiface.Option('PING_STR', 'Echo TCP', 'Message to send', required=False))

	def run(self):
		rhost = modiface.get_option_val('RHOST')
		rport = modiface.get_option_val('RPORT')
		timeout = modiface.get_option_val('TIMEOUT')
		send_delay = modiface.get_option_val('SEND_DELAY')
		send_message = modiface.get_option_val('PING_STR')
		while True:
			try:
				s = socket.create_connection((rhost, rport), timeout=timeout)
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
			print(buff)
			if buff[-1] in seps:
				end_recv = True
			yield buff
