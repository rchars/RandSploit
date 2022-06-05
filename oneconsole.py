import state.globals
import subprocess
import importlib
import readline
import pathlib
import atexit
import sys
import os


# GLOBALS
__KEYWORDS = {}


def console():
	while True:
		try:
			buff = input(state.globals.PROMPT_STR)
			if not buff:
				continue
			cmd = buff.split()
			cmd_len = len(cmd)
			state.globals.KEYWORD_CMD = cmd[1:]
			state.globals.KEYWORD_CMD_LEN = len(state.globals.KEYWORD_CMD)
			try:
				__KEYWORDS[cmd[0].upper()].execute()
			except KeyError:
				# nie dziala jak trzeba
				# problem z outputem
				shell_proc = subprocess.run(cmd, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				for info in (shell_proc.stdout, shell_proc.stderr):
					if info:
						print(info)
		except KeyboardInterrupt:
			print('')
		except EOFError:
			sys.exit()


def complete(text, state):
	if state == 0:
		if not text:
			for keyword_name in __KEYWORDS.keys():
				print(keyword_name)
		else:
			buff = text.split()
			state.globals.KEYWORD_COMPLETE_CMD = buff[1:-1]
			state.globals.KEYWORD_COMPLETE_CMD_LEN = len(state.globals.KEYWORD_COMPLETE_CMD)
			try:
				return __KEYWORDS[buff[0]].complete()
			except KeyError:
				return ''


def load_keywords():
	for keyword_path in state.globals.KEYWORDS_PATH.iterdir():
		try:
			if keyword_path.name.startswith('_'):
				continue
			keyword_mod = importlib.import_module(f'keywords.{keyword_path.stem}')
			keyword_inst = keyword_mod.Keyword()
			keyword_inst.execute
			keyword_inst.complete
			__KEYWORDS[keyword_inst.name] = keyword_inst
			del sys.modules[f'keywords.{keyword_path.stem}']
		except AttributeError:
			print(f'\'{keyword_path.name}\' is not a valid module')


if __name__ == '__main__':
	try:
		sys.path.append('..')
		state.globals.PROMPT_STR = 'frame>'
		state.globals.KEYWORDS_PATH = pathlib.Path('keywords')
		state.globals.MODULES_PATH = pathlib.Path('modules')
		state.globals.USER_MODULES_PATH = pathlib.Path().home() / pathlib.Path('.FrameworkOne/modules')
		state.globals.USER_MODULES_PATH.mkdir(parents=True, exist_ok=True)
		load_keywords()
		console()
	except(KeyboardInterrupt, EOFError):
		sys.exit()
