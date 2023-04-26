#!/usr/bin/python3 -B
import Interpreter.interpreter
import sys


if __name__ == '__main__':
	try:
		Interpreter.interpreter.start_interpreter()
	except(KeyboardInterrupt, EOFError):
		sys.exit('\n')


# TODO:
# Windows cmd support (non-standard package)
# ModUtils package
# IDEA:
# Linux SO injector module
# Network stuff module
# Session backgrounding
# Better exception handling
