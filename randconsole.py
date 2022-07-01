import cmd
import importlib.machinery
import os
import pathlib
import sys
import RandModHandle.RandModIface


# this must use pyclbr
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
					except Exception:
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
	
	# this may raise TypeError or AttibuteError
	def __validate_mod(self, mod):
		if not callable(mod.run) or not callable(mod.load_registers):
			raise TypeError
		elif type(mod.NAME) != str:
			raise TypeError

	def get_mod_by_name(self, name):
		for mod_dir in self.__modules_paths:
			for mod_path in mod_dir.iterdir():
				if mod_path.name.startswith('_') or not mod_path.is_file():
					continue
				try:
					mod = self.__get_mod_inst(mod_path)
					self.__validate_mod(mod)
					if mod.NAME == name:
						return mod
				except(TypeError, AttributeError):
					continue
		raise ValueError(f'No such module as \'{name}\'')


class Console(cmd.Cmd):
	def __init__(self, mod_manager):
		cmd.Cmd.__init__(self)
		self.prompt = 'frame>'
		self.call_dict = {
			'use': self.use,
			'help': self.the_help,
			'set': self.the_set,
			'exit': self.the_exit,
			'run': self.run,
			'back': self.back,
			'modules': self.modules,
			'registers': self.registers
		}
		self.completion_call_dict = {
			'use': self.comp_use,
			'help': self.compl_help,
			'set': self.compl_set,
		}
		self.keyword_list = []
		self.keyword_list_len = 0
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
			self.keyword_list_len = len(self.keyword_list)
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
	
	def __get_match(self, index=-1):
		try:
			match = self.keyword_list[index]
		except IndexError:
			match = ''
		return match
	
	def comp_use(self, *ignored):
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
			try:
				mod = self.mod_manager.get_mod_by_name(mod_name)
			except ValueError as mod_not_found_err:
				print(mod_not_found_err)
			else:
				try:
					RandModHandle.RandModIface.clear_regs()
					mod.load_registers()
				except Exception as reg_add_err:
					print(f'Cloudn\'t validate registers for module: \'{mod.NAME}\' -- {reg_add_err}')
					RandModHandle.RandModIface.clear_regs()
				else:
					self.active_module_regs = RandModHandle.RandModIface.REGS
					self.active_module = mod
					self.prompt = f'frame>{mod.NAME}>'

	def compl_help(self, *ignored):
		pass
	
	def the_help(self):
		'''Display help about keywords'''
		if self.keyword_list_len <= 0:
			for method_key, method in self.call_dict.items():
				print(f'{method_key}: {method.__doc__}')
		elif self.keyword_list_len >= 1:
			keyword = self.keyword_list[0]
			try:
				print(f'{keyword}: {self.call_dict[keyword].__doc__}')
			except KeyError:
				print(f'No such keyword as \'{keyword}\'')

	def compl_set(self, *ignored):
		matches = []
		if not self.active_module_regs or not self.active_module:
			return matches
		match = self.__get_match()
		for reg in self.active_module_regs:
			reg_name = reg[0]
			if reg_name.startswith(match) and reg_name != match:
				matches.append(reg_name)
		return matches

	def the_set(self):
		'''Sets an active module\'s registers'''
		if not self.active_module_regs or not self.active_module:
			print('Choose a module first')
		elif self.keyword_list_len <= 0:
			print('Need a register to set')
		else:
			for reg in self.active_module_regs:
				reg_name = reg[0]
				reg_name_list = reg_name.split()
				reg_name_list_len = len(reg_name_list)
				if self.keyword_list[0:reg_name_list_len] == reg_name_list:
					new_value = ' '.join(self.keyword_list[reg_name_list_len:])
					try:
						# not sure if it's possible that method'll raise an exception
						self.active_module_regs.update_reg(reg_name, new_value)
					except KeyError as reg_update_err:
						print(reg_update_err)
					break
			else:
				invalid_register_name = ' '.join(self.keyword_list)
				print(f'No such register as \'{invalid_register_name}\'')

	def the_exit(self):
		'''Exits script'''
		self.terminate_console = True
	
	def run(self):
		'''Runs active module'''
		if not self.active_module:
			print('Nothing to run')
		else:
			try:
				self.active_module.run()
			except Exception as module_err:
				print(module_err)

	def back(self):
		'''Unsets active module'''
		self.active_module = None
		self.active_module_regs = None
		self.prompt = 'frame>'
		RandModHandle.RandModIface.clear_regs()
	
	def registers(self):
		'''Displays a registers of the active module'''
		if not self.active_module_regs:
			print('Choose a module first')
		else:
			try:
				for reg_tupl in self.active_module_regs:
					print('{:<20} {:<15} {:<10}'.format(*reg_tupl))
			except Exception as invalid_reg:
				print(f'Cannot display registers: {invalid_reg}')

	def modules(self):
		'''Display all the avaiable modules'''
		for mod_index, mod in enumerate(self.mod_manager):
			print(f'{mod_index}: {mod.NAME}')


if __name__ == '__main__':
	try:
		# sys.path.append('..')
		modules_path = pathlib.Path('RandMods')
		# user_modules_path = pathlib.Path().home() / pathlib.Path('.FrameworkOne/OneModules')
		# user_modules_path.mkdir(parents=True, exist_ok=True)
		console_inst = Console(ModulesPathsManager(modules_path))
		console_inst.cmdloop()
	except(KeyboardInterrupt, EOFError):
		sys.exit('\n')
