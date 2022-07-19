import RandModHandle.RandModIface as ri

NAME = 'TestModule1'
DESCRIPTION = 'Module for toolkit test'
FIRST_VAL = 10

def valid_1(integer):
	if int(integer) < 10:
		raise ValueError('Value is too low')


def load_registers():
	ri.REGS.add_reg('Test', value=FIRST_VAL, description='testing',  validator=valid_1)


def run():
	print(f'The first val: {FIRST_VAL}')
