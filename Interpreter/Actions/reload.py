import Interpreter.Actions.use as u
import importlib.machinery as my
import Interpreter.state
import inspect


def execute():
	if not Interpreter.state.ACTIVE_MOD:
		return
	module = inspect.getmodule(Interpreter.state.ACTIVE_MOD)
	u.execute(module.__file__)
