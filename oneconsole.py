import ModulePattern.OneModuleIface
import cmd
import importlib.machinery
import os
import pathlib
import sys


class ModulesPathsManager:
	def __init__(self, *modules_paths):
		self.__modules_paths = modules_paths
		self.__paths_len = len(self.__modules_paths)
	
	def __iter__(self):
		self.__index = 0
		self.__current_path = self.__modules_paths[0].iterdir()
		return self
	
	def __next__(self):
		ret_mod = None
		while not ret_mod:
			try:
				mod_path = next(self.__current_path)
				if not mod_path.name.startswith('_'):
					try:
						mod = self.__get_mod_inst(mod_path)
						self.__validate_mod(mod)
					except(TypeError, AttributeError):
						continue
					ret_mod = mod
			except StopIteration:
				self.__index += 1
				if self.__index >= self.__paths_len:
					raise StopIteration
				self.__current_path = self.__modules_paths[self.__index].iterdir()
		return ret_mod
	
	def __get_mod_inst(self, path):
		return importlib.machinery.SourceFileLoader(path.stem, str(path.resolve())).load_module()
	
	# this can raise TypeError or AttibuteError
	def __validate_mod(self, mod):
		if not callable(mod.run):
			raise TypeError
		elif type(mod.NAME) != str:
			raise TypeError


class Console(cmd.Cmd):
	def __init__(self, mod_manager):
		cmd.Cmd.__init__(self)
		self.prompt = 'frame>'
		self.call_dict = {
			'use': self.use,
			'help': self.help,
			'set': self.set,
			'exit': self.exit,
			'run': self.run,
			'back': self.back,
			'registers': self.registers
		}
		self.completion_call_dict = {
			'use': self.complete_use,
			'help': self.complete_help,
			'set': self.complete_set,
		}
		self.keyword_list = []
		self.keyword_list_len = 0
		self.keyword_wordlist = []
		self.terminate_console = False
		self.mod_manager = mod_manager
		self.active_module = None
		self.active_module_regs = None
	
	def completenames(self, text, line, begidx, endidx):
		matches = []
		for keyword_name in self.call_dict.keys():
			if keyword_name.startswith(line.lower()):
				matches.append(keyword_name)
		return matches
	
	def completedefault(self, text, line, *ignored):
		matches = []
		words = line.split()
		keyword_name = words[0]
		if keyword_name in self.call_dict.keys():
			self.keyword_list = words[1:]
			matches = self.completion_call_dict[keyword_name]()
		return matches
	
	def onecmd(self, line):
		command_list = line.split()
		if len(command_list) >= 1:
			keyword_name = command_list[0]
			self.keyword_list = command_list[1:]
			self.keyword_list_len = len(self.keyword_list)
			try:
				self.call_dict[keyword_name]()
			except KeyError:
				os.system(line)
		return self.terminate_console
	
	def __get_match(self, index=1):
		try:
			match = self.keyword_list[index]
		except IndexError:
			match = ''
		return match
	
	def complete_use(self, *ignored):
		match_str = self.__get_match()
		matched_mods = []
		for mod in self.mod_manager:
			if mod.NAME.startswith(match_str) and mod.NAME not in matched_mods:
				matched_mods.append(mod.NAME)
		return matched_mods
	
	def use(self):
		'''Use a module'''
		try:
			mod_name = self.keyword_list[0]
		except IndexError:
			print('Need a module name')
		else:
			for mod in self.mod_manager:
				if mod.NAME == mod_name:
					try:
						# the table is unvalidated, it may be corrupted
						mod.load_registers()
						self.active_module_regs = ModulePattern.OneModuleIface.REGISTERS_TABLE
					except Exception:
						self.active_module_regs = {}
					self.active_module = mod
					break
			else:
				print(f'No such module as \'{mod_name}\'')
	
	def complete_help(self, *ignored):
		pass
	
	def help(self):
		'''Display help about keywords'''
		pass
	
	def complete_set(self, *ignored):
		pass
	
	def set(self):
		'''Sets an active module\'s registers'''
		pass
	
	def exit(self):
		'''Exits script'''
		pass
	
	def run(self):
		'''Runs active module'''
		pass
	
	def back(self):
		'''Unsets active module'''
		pass
	
	def registers(self):
		'''Displays a registers of the active module'''
		


if __name__ == '__main__':
	try:
		# sys.path.append('..')
		modules_path = pathlib.Path('OneModules')
		# user_modules_path = pathlib.Path().home() / pathlib.Path('.FrameworkOne/OneModules')
		# user_modules_path.mkdir(parents=True, exist_ok=True)
		console_inst = Console(ModulesPathsManager(modules_path))
		console_inst.cmdloop()
	except(KeyboardInterrupt, EOFError):
		sys.exit()
