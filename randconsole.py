#!/usr/bin/python3 -B
import Interpreter.interpreter
import sys


if __name__ == '__main__':
	try:
		Interpreter.interpreter.start_interpreter()
	except(KeyboardInterrupt, EOFError):
		sys.exit('\n')
	except ModuleNotFoundError as mod_err:
		print(mod_err)
		sys.exit('\n')


# TODO:
# Proxy package for module building
# Better exception handling
# Session backgrounding
# ModUtils package
# VENV
# IDEA:
# Linux SO injector module
# Network stuff module
