import ModInterface.ModInterface as m
import importlib.machinery as my
import inspect
import pathlib


class __ModBuilder:
	@staticmethod
	def __getattr__(opt_name):
		option = pathlib.Path('Option') / pathlib.Path(f'{opt_name}.py')
		return my.SourceFileLoader(opt_name, str(option)).load_module().Opt


Builder = __ModBuilder()
ModIface = m.ModInterface
