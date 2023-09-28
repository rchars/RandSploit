import Interpreter.state as state
import tabulate


def generate():
	for mod_dir in state.MOD_DIRS:
		for mod_path in mod_dir.iterdir():
			if mod_path.suffix == '.py':
				yield [str(mod_path)]


def execute():
	'''Get a list of all modules.'''
	print(
		tabulate.tabulate(
			generate(),
			showindex='always',
			tablefmt=state.TABLEFMT
		)
	)
