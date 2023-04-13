import Interpreter.StateUtils as su
import Interpreter.state as state


def execute(text):
	if not text:
		print('Use what ?')
	else:
		try:
			mod_id = int(text)
		except ValueError:
			mod_id = text
		for mod_dir in state.MOD_DIRS:
			for index, mod_path in enumerate(mod_dir.iterdir()):
				if mod_id == index or mod_id == str(mod_path):
					state.ACTIVE_MOD = su.get_mod_inst(mod_path)
					state.PROMPT = mod_path.stem + '>'
					return None
		else:
			raise FileNotFoundError('Standard msg, you know what to do')
