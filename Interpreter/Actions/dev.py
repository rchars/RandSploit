import Interpreter.state as state


def execute(text):
	'''Enable developer mode (verbose exceptions).'''
	if not text or 'help'.startswith(text.lower()):
		print(
			'dev frame => Toggle the frame developer mode.\n' +
			'dev mod => Toggle the module developer mode.\n',
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


def complete(text):
	if not text: return ['frame', 'mod']
	if 'frame'.startswith(text): return ['frame']
	elif 'mod'.startswith(text): return ['mod']


# def execute():
# 	'''Enable developer mode (verbose exceptions).'''
# 	if not Interpreter.state.DEV:
# 		Interpreter.state.DEV = True
# 		print('Developer mode on')
# 	else:
# 		Interpreter.state.DEV = False
# 		print('Developer mode off')
