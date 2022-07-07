import RandModHandle.RandModIface
import socket
import time


NAME = 'PORT_FUZZ'


def load_registers():
	RandModHandle.RandModIface.REGS.add_reg('RHOST')
	RandModHandle.RandModIface.REGS.add_reg('RPORT')


def run():
	rhost = RandModHandle.RandModIface.REGS.get_reg('RHOST').value
	rport = RandModHandle.RandModIface.REGS.get_reg('RPORT').value
	bomb_size = 100
	bomb_char = b'A'
	while True:
		s = socket.socket()
		s.settimeout(0.5)
		s.connect((rhost, int(rport)))
		s.send(bomb_size * bomb_char)
		print(f'Bomb size == {bomb_size}')
		time.sleep(0.1)
		bomb_size += 100
