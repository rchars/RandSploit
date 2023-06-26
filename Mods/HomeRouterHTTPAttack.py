import ModBuilder.ModBuilder as mb
import socket

req = '''GET /2.0/gui/ HTTP/1.1
Host: {}
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1


'''.replace('\n', '\r\n')

class Mod(mb.ModIface):
	def __init__(self):
		self.rhost = mb.Opt.DefaultOpt.Opt('RHOST', 'localhost')
		self.rport = mb.Opt.ValidatedOpt.Opt('RPORT', value=9999, validator=int)

	def run(self):
		while True:
			client_sock = socket.create_connection((self.rhost.value, self.rport.value))
			client_sock.send(req.encode())
			handle_recv = mb.Util.Net.RecvLines(client_sock)
			for line in handle_recv.recv_till_dead():
				print(line, end='')
			print(handle_recv.reminder)
			print(handle_recv.death_reason)
