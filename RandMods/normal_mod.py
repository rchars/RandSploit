import RandModHandle.RandModIface
import socket

NAME = 'NormalModule'

# RandModHandle.RandModIface.REGS.add_reg('fsfs', '', '')

def load_registers():
	RandModHandle.RandModIface.REGS.add_reg('RHOST', '', 'TARGET')
	RandModHandle.RandModIface.REGS.add_reg('PORT', None, 'the ports of the target')


def run():
	host = RandModHandle.RandModIface.REGS.get_reg('RHOST').value
	port = int(RandModHandle.RandModIface.REGS.get_reg('PORT').value)
	s = socket.socket()
	s.connect((host, port))
	s.send(b'fidfhvisdhf g;sdfj igsafdhgiposdfhgoidfshuiogdfshig')
