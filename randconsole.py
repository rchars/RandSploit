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
# Session backgrounding (difficult)
# Option templates (enlarge)
# Util package (enlarge)
# Better reload command
# Editor option
# Better pip handling
# Help for the options
# IDEA:
# Linux SO injector module
# Network stuff module
# HTTPLinkSearch
# HTTPRequest
# DNSResolver
# TCPProxy
