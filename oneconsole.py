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
			state.globals.KEYWORD_CMD = cmd[1:-1]
			try:
				# execute printuje wyniki, nie zwraca ich
				# bo nawet nie wiem czy jest sens
				__KEYWORDS[cmd[0]].execute()
			except KeyError:
				# nie mam pojecia czemu to nie dziala jak trzeba
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
			try:
				return __KEYWORDS[buff[0]].complete(buff[1:-1])
			except KeyError:
				return ''


def load_keywords():
	for keyword_path in state.globals.KEYWORDS_PATH.iterdir():
		try:
			if keyword_path.name.startswith('_'):
				continue
			keyword_mod = importlib.import_module(keyword_path.name, package='keywords')
			keyword_inst = keyword_mod.Keyword()
			keyword_inst.execute
			keyword_inst.complete
			__KEYWORDS[keyword_inst.name] = keyword_inst
			del sys.modules[keyword_inst.name]
		except AttributeError:
			print(f'\'{keyword_path.name}\' is not a valid module')
	

if __name__ == '__main__':
	try:
		# jak to nie zadziala
		# to klawiatury nie pozaluje
		sys.path.append('..')
		state.globals.PROMPT_STR = 'frame>'
		state.globals.KEYWORDS_PATH = pathlib.Path('keywords')
		load_keywords()
		console()
	except(KeyboardInterrupt, EOFError):
		sys.exit()


# Czego jeszcze brakuje:
# Interfejsu modolow specjalnych
# Jakichkolwiek modulow
