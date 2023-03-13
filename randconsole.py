import ModManagement.ModManager
import importlib.machinery
import traceback
import pathlib
import cmd
import sys


class Interpreter(cmd.Cmd):
	def __init__(self, mod_manager):
		self.mod_manager = mod_manager

	def default(self, line):
		print(f'No such command as \'{line}\'')

	def do_mods(self, line):
		# print table of mods
		pass
	
	def do_back(self, line):
		self.mod_manager.unroll_mod()

if __name__ == '__main__':
	try:
		global_mods_path = pathlib.Path(__file__).resolve().parent / pathlib.Path('mods')
		user_mods_path = pathlib.Path().home() / pathlib.Path('.randmods')
		mod_path_manager = ModManagement.ModPathManager(global_mods_path, user_mods_path)
		Interpreter(mod_path_manager).cmdloop()
	except KeyboardInterrupt:
		sys.exit('Bye!\n')