import RandModHandle.RandModIface
import socket


NAME = 'NormalModule'


def load_registers():
	RandModHandle.RandModIface.REGS.add_reg('RHOST', '', 'TARGET')
	RandModHandle.RandModIface.REGS.add_reg('PORT', None, 'the ports of the target', reg_type=list)


def run():
	host = RandModHandle.RandModIface.get_reg('RHOST').value
	port = RandModHandle.RandModIface.get_reg('PORT').value
	s = socket.socket()
	s.connect((host, port))
	s.send(b'fidfhvisdhf g;sdfj igsafdhgiposdfhgoidfshuiogdfshig')