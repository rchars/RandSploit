import Interpreter.state as state


def execute(text):
	'''Enable developer mode (verbose exceptions).'''
	if not text:
		print(
			'dev frame\n' +
			'dev mod\n',
			end=''
		)
		return
	modes = {
		'frame': state.FRAME_DEV,
		'mod': state.MOD_DEV
	}
	if not text in modes.keys():
		raise ValueError(f'There is no such mode as \'{text}\'')
	gate_to_toggle = modes[text]
	gate_to_toggle.toggle()
	print(f'{gate_to_toggle.name} mode => {gate_to_toggle}')


# def execute():
# 	'''Enable developer mode (verbose exceptions).'''
# 	if not Interpreter.state.DEV:
# 		Interpreter.state.DEV = True
# 		print('Developer mode on')
# 	else:
# 		Interpreter.state.DEV = False
# 		print('Developer mode off')
