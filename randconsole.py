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

	def do_run(self, line):
		try:
			self.mod_manager.run_mod()
		except Exception:
			traceback.print_exc()

	def do_use(self, line):
		# we interact with untrusted code, so catch all exceptions
		try:
			pass
		except Exception:
			traceback.print_exc()
		
	def do_mods(self, line):
		# transmutate it onto interable
		# print table of mods
		pass
	
	def do_back(self, line):
		self.mod_manager.unroll_mod()

	def do_exit(self, line):
		print('Bye\n')
		return True

	do_EOF = do_exit

if __name__ == '__main__':
	try:
		global_mods_path = pathlib.Path(__file__).resolve().parent / pathlib.Path('mods')
		user_mods_path = pathlib.Path().home() / pathlib.Path('.randmods')
		mod_path_manager = ModManagement.ModManager(global_mods_path, user_mods_path)
		Interpreter(mod_path_manager).cmdloop()
	except KeyboardInterrupt:
		sys.exit('Bye!\n')


# Can't change:
# ModInterface
# Option
# Can change:
# UserOptions
# Mods

# NOTE:
# Be careful how you create interfaces, cuz they cannot change
# If you will fuck something, refactor it ASAP


# Now I have to think about modules creation
# first, module is extension of the interface class but it's ducky typed, so I ll just catch exceptions and wont be fucking arround data validation
# the ModInterface must contain the list that stores the options that are created on OptionInterface and again - it's ducky typed
