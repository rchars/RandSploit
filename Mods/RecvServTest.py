import ModBuilder.ModBuilder as mb
import socket


class Mod(mb.ModIface):
	def run(self):
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('localhost', 9999))
		s.listen(1)
		while True:
			c = s.accept()[0]
			c.settimeout(3)
			try:
				while True:
					data = c.recv(6144)
					print(data.decode())
					c.send('Echo: '.encode() + data)
			except socket.timeout:
				c.close()
