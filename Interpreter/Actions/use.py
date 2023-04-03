import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, tokens):
		if not tokens:
			print('Use what ?')
		else:
			state.STATE.active_mod = state.STATE.get_action_mod(tokens[0])
