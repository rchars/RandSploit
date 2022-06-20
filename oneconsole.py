import state.globals
import importlib
import readline
import pathlib
import atexit
import cmd
import sys
import os


class ModulesPathsManager:
	def __init__(self, *modules_paths):
		self.__modules_paths = modules_paths
		self.__paths_len = len(self.__modules_paths)

	def __iter__(self):
		self.__index = 0
		self.__current_path = self.__modules_paths[0].iterdir()
		return self

	def __next__(self):
		ret_path = None
		while not ret_path:
			try:
				mod_path = next(self.__current_path)
				if not mod_path.name.startswith('_'):
					ret_path = mod_path
			except StopIteration:
				self.__index += 1
				if self.__index >= self.__paths_len:
					raise StopIteration
				self.__current_path = self.__modules_paths[self.__index].iterdir()
		return ret_path


class Console(cmd.Cmd):
	def __init__(self, keywords):
		self.__keywords = keywords
		self.prompt = state.globals.PROMPT_STR
		cmd.Cmd.__init__(self)

	def completenames(self, text, line, begidx, endidx):
		ret_val = []
		buff = line.upper().split()
		buff_len = len(buff)
		if not buff:
			ret_val = list(self.__keywords.keys())
		elif buff_len == 1:
			for keyword in self.__keywords.keys():
				if keyword.startswith(buff[0]):
					ret_val.append(keyword)
		return ret_val

	def completedefault(self, text, line, *ignored):
		complete_list = []
		list_line = line.upper().split()
		self.__update_cmd(list_line[1:])
		try:	
			complete_list = self.__keywords[list_line[0]].complete()
		except(KeyError, AttributeError):
			pass
		finally:
			return complete_list
	
	def postcmd(self, stop, line):
		cmd = line.split()
		if not cmd:
			return False
		try:
			self.__update_cmd(cmd[1:])
			self.__keywords[cmd[0].upper()].execute()
		except KeyError:
			os.system(line)
		except Exception as keyword_err:
			print(keyword_err)
		finally:
			return state.globals.EXIT_SCRIPT
		
	# No idea what to do with this
	def default(self, line):
		pass


	def __update_cmd(self, cmd):
		state.globals.KEYWORD_CMD = cmd
		state.globals.KEYWORD_CMD_LEN = len(cmd)


def load_keywords():
	ret_keywords = {}
	for keyword_path in state.globals.KEYWORDS_PATH.iterdir():
		try:
			if keyword_path.name.startswith('_'):
				continue
			keyword_mod = importlib.import_module(f'keywords.{keyword_path.stem}')
			keyword_inst = keyword_mod.Keyword()
			keyword_inst.execute
			keyword_inst.complete
			ret_keywords[keyword_inst.name] = keyword_inst
			del sys.modules[f'keywords.{keyword_path.stem}']
		except AttributeError:
			print(f'\'{keyword_path.name}\' is not a valid module')
	else:
		return ret_keywords


if __name__ == '__main__':
	try:
		sys.path.append('..')
		state.globals.PROMPT_STR = 'frame>'
		state.globals.KEYWORDS_PATH = pathlib.Path('keywords')
		modules_path = pathlib.Path('modules')
		user_modules_path = pathlib.Path().home() / pathlib.Path('.FrameworkOne/modules')
		user_modules_path.mkdir(parents=True, exist_ok=True)
		state.globals.MODULE_MANAGER = ModulesPathsManager(user_modules_path, modules_path)
		console_inst = Console(load_keywords())
		console_inst.cmdloop()
	except(KeyboardInterrupt, EOFError):
		sys.exit()
