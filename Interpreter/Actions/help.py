import importlib.machinery as mach
import Interpreter.state as state
import tabulate


def generate():
	for action_dir in state.ACTION_DIRS:
		for action_mod_path in action_dir.iterdir():
			if not action_mod_path.is_file(): continue
			action_mod_inst = mach.SourceFileLoader(action_mod_path.name, str(action_mod_path)).load_module()
			try:
				doc = action_mod_inst.execute.__doc__
			except AttributeError:
				doc = 'Undocumented.'
			else:
				if not action_mod_inst.execute.__doc__:
					doc = 'Undocumented.'
			yield [action_mod_path.stem, doc]


def execute():
	'''Print this page.'''
	print(
		tabulate.tabulate(
			generate(),
			showindex='never',
			tablefmt=state.TABLEFMT
		)
	)