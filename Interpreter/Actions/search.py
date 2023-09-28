import Interpreter.state as state
import tabulate
import re


def search(regex):
	index = 0
	for mod_dir in state.MOD_DIRS:
		for mod_path in mod_dir.iterdir():
			if not mod_path.is_file():
				continue
			re_obj = re.search(regex, str(mod_path.name))
			if re_obj != None: yield (index, mod_path)
			index += 1


def execute(regex=''):
	'''Search for a module.'''
	print(
		tabulate.tabulate(search(regex), tablefmt=state.TABLEFMT)
	)
