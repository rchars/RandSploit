import RandSploitModules.ModulePathManager
import RandSploitModules.RegisterManager
import RandModHandle.RandModIface
import itertools
import inspect
import pathlib
import cmd
import sys
import os


class KeywordHandler:
	def __init__(self, prompt, mod_manager):
		self.prompt = prompt
		self.keyword_list = []
		self.keyword_list_len = 0
		self.terminate_console = False
		self.mod_manager = mod_manager
		self.modules_num_cache = {}
		self.active_module = None
		self.active_module_regs = None

	def __get_match(self, index=-1):
		try:
			match = self.keyword_list[index]
		except IndexError:
			match = ''
		return match

	def compl_use(self):
		match_str = self.__get_match()
		matched_mods = []
		for mod in self.mod_manager:
			if mod.NAME.startswith(match_str) and mod.NAME not in matched_mods:
				matched_mods.append(mod.NAME)
		return matched_mods

	# what if module name is a digit
	def keyword_use(self):
		'''Use a module'''
		try:
			mod_name = self.keyword_list[0]
		except IndexError:
			print('Need a module name')
		else:
			def activate_mod(mod):
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
			if mod_name.isdigit():
				try:
					activate_mod(self.modules_num_cache[int(mod_name)])
				except KeyError:
					print(f'No such module as \'{mod_name}\'')
			else:
				try:
					mod = self.mod_manager.get_mod_by_name(mod_name)
				except ValueError as mod_not_found_err:
					print(mod_not_found_err)
				else:
					activate_mod(mod)

	def compl_set(self):
		matches = []
		if not self.active_module_regs or not self.active_module:
			return matches
		match = self.__get_match()
		for reg in self.active_module_regs:
			reg_name = reg[0]
			if reg_name.startswith(match) and reg_name != match:
				matches.append(reg_name)
		return matches

	def keyword_set(self):
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
						print(f'{reg_name} => {new_value}')
					except KeyError as reg_update_err:
						print(reg_update_err)
					break
			else:
				invalid_register_name = ' '.join(self.keyword_list)
				print(f'No such register as \'{invalid_register_name}\'')

	def keyword_exit(self):
		'''Exits script'''
		self.terminate_console = True
	
	def keyword_run(self):
		'''Runs active module'''
		if not self.active_module:
			print('Nothing to run')
		else:
			try:
				self.active_module.run()
			except Exception as module_err:
				print(module_err)
			except KeyboardInterrupt:
				print()

	def keyword_back(self):
		'''Unsets active module'''
		self.active_module = None
		self.active_module_regs = None
		self.prompt = 'frame>'
		RandModHandle.RandModIface.clear_regs()

	# not done yet
	def keyword_registers(self):
		'''Displays a registers of the active module'''
		if not self.active_module_regs:
			print('Choose a module first')
		else:
			try:
				self.print_table(RandSploitModules.RegisterManager.RegisterManagerWrapper(self.active_module_regs))
			except Exception as invalid_reg:
				print(f'Cannot display registers: {invalid_reg}')

	def keyword_modules(self):
		'''Display all the avaiable modules'''
		self.print_table(RandSploitModules.ModulePathManager.TableWrapper(self.mod_manager))
	
	def print_table(self, table_obj):
		lenghts = []
		for column in zip(*table_obj):
			lenghts.append(max([len(str(field)) for field in column]))
		for row in table_obj:
			print_str = ''
			for field, replenish_len in zip(row, lenghts):
				field_len = len(str(field))
				real_len = replenish_len - field_len
				print_str += '{}' + ' ' * real_len + ' | '
			print(print_str.format(*row))
			

class Console(cmd.Cmd):
	def __init__(self, mod_manager):
		cmd.Cmd.__init__(self)
		self.keyword_handler = KeywordHandler('frame>', mod_manager)
		self.prompt = self.keyword_handler.prompt
		self.handler_calldict = {}
		self.handler_compldict = {}
		for met in inspect.getmembers(self.keyword_handler, predicate=inspect.ismethod):
			if met[0].startswith('keyword'): self.handler_calldict[met[0][8:]] = met[1]
			elif met[0].startswith('compl'): self.handler_compldict[met[0][6:]] = met[1]

	def completenames(self, text, line, begidx, endidx):
		matches = []
		for keyword_name in self.handler_calldict.keys():
			if keyword_name.startswith(line.lower()):
				matches.append(keyword_name)
		return matches

	def completedefault(self, text, line, *ignored):
		matches = []
		words = line.split()
		keyword_name = words[0]
		if keyword_name in self.handler_compldict.keys():
			self.keyword_handler.keyword_list = words[1:]
			self.keyword_handler.keyword_list_len = len(self.keyword_handler.keyword_list)
			matches = self.handler_compldict[keyword_name]()
		return matches

	def onecmd(self, line):
		command_list = line.split()
		if len(command_list) >= 1:
			keyword_name = command_list[0]
			self.keyword_handler.keyword_list = command_list[1:]
			self.keyword_handler.keyword_list_len = len(self.keyword_handler.keyword_list)
			try:
				self.handler_calldict[keyword_name]()
				self.prompt = self.keyword_handler.prompt
			except KeyError:
				os.system(line)
		return self.keyword_handler.terminate_console


if __name__ == '__main__':
	try:
		modules_path = pathlib.Path('RandMods')
		# user_modules_path = pathlib.Path().home() / pathlib.Path('.FrameworkOne/OneModules')
		# user_modules_path.mkdir(parents=True, exist_ok=True)
		console_inst = Console(RandSploitModules.ModulePathManager.ModulePathManager(modules_path))
		console_inst.cmdloop()
	except(KeyboardInterrupt, EOFError):
		sys.exit('\n')
