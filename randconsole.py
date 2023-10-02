#!/usr/bin/python3 -B
import Interpreter.interpreter
import sys


if __name__ == '__main__':
	try:
		Interpreter.interpreter.start_interpreter()
	except(KeyboardInterrupt, EOFError):
		sys.exit('Bye!\n')
	except ModuleNotFoundError as mod_err:
		print(mod_err)
		sys.exit('\n')


# TODO:
# Documentation
# Better exception handling
# Session backgrounding
# VENV
# IDEA:
# Linux SO injector module
# Network stuff module
