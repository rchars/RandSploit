import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, tokens):
		if not tokens:
			print('Use what ?')
		else:
			state.STATE.active_mod = state.STATE.get_module_by_id(tokens[0])

	# Not sure about the tokens parameter
	# The parameter will be path for sure
	def complete(self, tokens):
		pass
