import Interpreter.state as state


def execute(self):
	if state.ACTIVE_MOD is None:
		print('Select mod before executing')
	else:
		try:
			state.ACTIVE_MOD.run()
		except(KeyboardInterrupt, EOFError):
			print()
