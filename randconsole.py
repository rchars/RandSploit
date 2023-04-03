import Interpreter.interpreter
import sys


if __name__ == '__main__':
	try:
		Interpreter.interpreter.start_interpreter()
	except(KeyboardInterrupt, EOFError):
		sys.exit('\n')
