import socket


class RecvLines:
	_reminder = ''
	_death_reason = ''

	def __init__(self, tcp_sock, buff_size=1024):
		self.tcp_sock = tcp_sock

	def recv_till_dead(self, buff_size=1024):
		try:
			while(buff := self.tcp_sock.recv(buff_size).decode()) and buff != '':
				try:
					while eol_pos := buff.index('\n'):
						yield self._reminder + buff[0:eol_pos + 1]
						buff = buff[eol_pos + 1:]
						self._reminder = ''
				except ValueError:
					self._reminder += buff
		except(OSError, socket.timeout) as e:
			self._death_reason = e
		finally:
			self.tcp_sock.close()

	@property
	def reminder(self):
		return self._reminder

	@property
	def death_reason(self):
		return self._death_reason

