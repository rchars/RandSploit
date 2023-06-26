import ModInterface.ModInterface as m
import importlib.machinery as my
import pathlib


class _AutoModProvider:
	def __init__(self, exc_ins, search_dir):
		self.search_dir = search_dir
		self.exc_ins = exc_ins

	def __getattr__(self, mod_name):
		mod_path = pathlib.Path(f'{self.search_dir}') / pathlib.Path(f'{mod_name}.py')
		if not mod_path.is_file():
			raise FileNotFoundError(
				f'No such {self.exc_ins} as \'{mod_name}\''
			)
		return my.SourceFileLoader(
			mod_name,
			str(mod_path)
		).load_module()


ModIface = m.ModInterface
Util = _AutoModProvider('util', 'Util')
Opt = _AutoModProvider('opt', 'Option')
