import importlib.machinery as my
import pathlib as pb
import traceback
import randstate
import modiface
import cmd
import sys


class ModPathManager:
	def __init__(self, *dirs):
		if not dirs:
			raise ValueError('Dirs cannot be empty')
		self.dirs = dirs
		self.dirs_len = len(self.dirs)

	def set_iter_dir(self):
		try:
			self.iter_dir = iter(self.dirs[self.dir_index].iterdir())
		except IndexError:
			raise StopIteration

	def __iter__(self):
		self.mod_index = 0
		self.dir_index = 0
		self.set_iter_dir()
		return self

	def __next__(self):
		while True:
			mod_path = next(self.iter_dir)
			if mod_path is None:
				self.dir_index += 1
				self.set_iter_dir()
			elif mod_path.is_file():
				self.mod_index += 1
				break
		return self.mod_index, mod_path.resolve()

	def get_mod_path(self, mod_id, index=False):
		for the_dir in self.dirs:
			mod_index = 1
			for mod_path in the_dir.iterdir():
				if not mod_path.is_file():
					continue
				elif str(mod_index) == mod_id or str(mod_path.resolve()) == mod_id:
					if not index:
						return mod_path
					return mod_path, mod_index
				mod_index += 1
		raise ValueError(f'Module \'{mod_id}\' not found')


class TransformOptions:
	def __init__(self, options):
		self.options = options

	def __iter__(self):
		self.option_index = None
		return self

	def __next__(self):
		try:
			if self.option_index is None:
				self.option_index = 0
				return 'name', 'value', 'description', 'required'
			option = self.options[self.option_index]
			self.option_index += 1
			try:
				req = option.required
			except AttributeError:
				req = False
			return option.name, option.val, option.description, req
		except IndexError:
			raise StopIteration


class TransformModules:
	def __init__(self, mod_path_manager):
		self.mod_path_manager = mod_path_manager

	def __iter__(self):
		self.iter_mod_path_manager = None
		return self

	def __next__(self):
		if self.iter_mod_path_manager is None:
			self.iter_mod_path_manager = iter(self.mod_path_manager)
			return '^', 'Name', 'Description'
		next_mod = next(self.iter_mod_path_manager)
		if next_mod is None:
			raise StopIteration
		return next_mod[0], next_mod[1]


class Interpreter(cmd.Cmd):
	def __init__(self):
		self.active_module = None
		self.defualt_prompt = 'rand>'
		self.prompt = self.defualt_prompt
		global_mods_path = pb.Path(__file__).resolve().parent / pb.Path('mods')
		user_mods_path = pb.Path().home() / pb.Path('.randmods')
		user_mods_path.mkdir(exist_ok=True)
		self.mod_path_manager = ModPathManager(
			global_mods_path,
			user_mods_path
		)
		super().__init__()

	def default(self, line):
		print(f'No such command as \'{line}\'')

	def print_table(self, table_obj):
		the_len = []
		for column in zip(*table_obj):
			the_len.append(max([len(str(field)) for field in column]))
		for row in table_obj:
			print_str = ''
			for field, replenish_len in zip(row, the_len):
				field_len = len(str(field))
				real_len = replenish_len - field_len
				print_str += '{}' + ' ' * real_len + ' # '
			real_print_str = '# ' + print_str.format(*row)
			real_tabular_str = (len(real_print_str) - 1) * '#'
			print(real_tabular_str)
			print(real_print_str)
		print(real_tabular_str)

	def do_options(self, line):
		if self.active_module is None:
			print('Choose a module first')
		elif randstate.MOD_OPTIONS is None:
			print(f'Module \'{self.active_module.name}\' has no options')
		else:
			self.print_table(TransformOptions(randstate.MOD_OPTIONS))

	def do_mods(self, line):
		self.print_table(TransformModules(self.mod_path_manager))

	def do_back(self, line):
		self.prompt = self.defualt_prompt
		randstate.MOD_OPTIONS = []
		self.active_module = None

	def do_exit(self, line):
		print('\nbye!\n')
		return True
	
	def do_run(self, line):
		if self.active_module is None:
			print('Choose a mod first')
		else:
			try:
				modiface.check_required()
				try:
					self.active_module.run()
				except Exception:
					traceback.print_exc()
			except Exception as valid_err:
				print(valid_err)
			except(KeyboardInterrupt, EOFError):
				print()

	def do_use(self, line):
		try:
			words = line.split()
			mod_id = words[0]
		except IndexError:
			print('Need a module index or name')
		else:
			try:
				mod_path, mod_index = self.mod_path_manager.get_mod_path(mod_id, index=True)
				mod = my.SourceFileLoader(mod_path.stem, path=str(mod_path.resolve())).load_module()
				self.do_back(None)
				mod_inst = mod.Mod()
				self.active_module = mod_inst
				if not self.active_module.prompt:
					prompt_str = f'{mod_index}>'
				else:
					prompt_str = self.active_module.prompt
				self.prompt = prompt_str
			except KeyboardInterrupt:
				self.do_back(None)
				print()
			except Exception:
				traceback.print_exc()
				self.do_back(None)

	def do_set(self, line):
		if not self.active_module:
			print('Choose a module first')
		else:
			try:
				words = line.split()
				option_name = words[0]
			except IndexError:
				print('Need an option\'s name')
			else:
				try:
					option_val = words[1]
				except IndexError:
					print('Need a value')
				else:
					try:
						modiface.set_option_val(option_name, option_val)
						print(f'{option_name} => {option_val}')
					except ValueError as val_not_found_err:
						print(val_not_found_err)
					except Exception as val_set_err:
						print(val_set_err)

	def complete_set(self, text, line, begidx, endidx):
		complete_words = []
		words = line.split()[1:]
		if self.active_module is None:
			return complete_words
		try:
			option_name = words[0]
		except IndexError:
			option_name = ''
		for option in randstate.MOD_OPTIONS:
			if option.name.startswith(' '.join(words)) and option.name != option_name:
				complete_words.append(option.name)
		return complete_words


if __name__ == '__main__':
	try:
		Interpreter().cmdloop()
	except KeyboardInterrupt:
		sys.exit('bye!\n')


# TODO:
# ModulePathManager class
# Interpreter class
# Interface for modules
# Fix everything
