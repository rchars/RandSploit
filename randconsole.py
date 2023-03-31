import Interpreter
import sys


if __name__ == '__main__':
	try:
		Interpreter.Interpreter.start_interpreter()
	except(KeyboardInterrupt, EOFError):
		sys.exit()
