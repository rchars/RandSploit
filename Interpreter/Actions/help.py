import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, tokens):
		for action_mod in state.STATE.iter_actions():
			print(action_mod.stem)
