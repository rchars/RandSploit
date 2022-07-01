import ModulePattern.OneModuleIface
import socket


NAME = 'NormalModule'


def load_registers():
	ModulePattern.OneModuleIface.REGS.add_reg('RHOST', '', 'TARGET')
	ModulePattern.OneModuleIface.REGS.add_reg('PORT', None, 'the ports of the target', reg_type=list)


def run():
	host = ModulePattern.OneModuleIface.get_reg('RHOST').value
	port = ModulePattern.OneModuleIface.get_reg('PORT').value
	s = socket.socket()
	s.connect((host, port))
	s.send(b'fidfhvisdhf g;sdfj igsafdhgiposdfhgoidfshuiogdfshig')