import importlib.machinery as mach
import Interpreter.state as state
import tabulate
import inspect


def generate():
	for action_dir in state.ACTION_DIRS:
		for action_mod_path in action_dir.iterdir():
			action_mod_inst = mach.SourceFileLoader(action_mod_path.name, str(action_mod_path)).load_module()
			try:
				doc = action_mod_inst.execute.__doc__
			except AttributeError as e:
				doc = e
			if not doc:
				doc = 'undocumented'
			yield [action_mod_path.stem, doc]


def execute(self):
	print(
		tabulate.tabulate(
			generate(),
			showindex='never',
			tablefmt=state.TABLEFMT
		)
	)
