import Interpreter.state


def execute():
	'''Enable developer mode (verbose exceptions).'''
	if not Interpreter.state.DEV:
		Interpreter.state.DEV = True
		print('Developer mode on')
	else:
		Interpreter.state.DEV = False
		print('Developer mode off')
