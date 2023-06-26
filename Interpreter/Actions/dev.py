import Interpreter.state


def execute():
	if Interpreter.state.DEV:
		Interpreter.state.DEV = False
		print('Developer mode on')
	else:
		Interpreter.state.DEV = True
		print('Developer mode off')
