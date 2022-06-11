import state.globals
import importlib
import readline
import pathlib
import atexit
import cmd
import sys
import os


class Console(cmd.Cmd):
	def __init__(self, keywords):
		self.__keywords = keywords
		self.prompt = state.globals.PROMPT_STR
		# self.identchars = list(keywords.keys())
		super().__init__()

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
		else:
			try:
				self.__update_cmd(buff[1:-1])
				ret_val = self.__keywords[buff[0]].complete().split()
			except(KeyError, AttributeError):
				return ret_val
		return ret_val

	def postcmd(self, stop, line):
		cmd = line.split()
		cmd_len = len(cmd)
		if not cmd:
			return False
		try:
			self.__update_cmd(cmd[1:-1])
			self.__keywords[cmd[0]].execute()
		except KeyError:
			os.system(line)
		except Exception as keyword_err:
			print(keyword_err)
		finally:
			return False

	# dont know what to do with this
	# this must be here for error
	# supressing
	def default(self, line):
		pass

	def __update_cmd(self, cmd):
		state.globals.KEYWORD_CMD = cmd
		state.globals.KEYWORD_CMD_LEN = len(cmd)



# This works well
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
		state.globals.MODULES_PATH = pathlib.Path('modules')
		state.globals.USER_MODULES_PATH = pathlib.Path().home() / pathlib.Path('.FrameworkOne/modules')
		state.globals.USER_MODULES_PATH.mkdir(parents=True, exist_ok=True)
		console_inst = Console(load_keywords())
		console_inst.cmdloop()
	except(KeyboardInterrupt, EOFError):
		sys.exit()