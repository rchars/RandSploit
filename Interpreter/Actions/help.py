import Interpreter.ActionInterface as ai
import Interpreter.state as state
import tabulate


class Action(ai.ActionInterface):
	def execute(self):
		for action_mod in state.STATE.iter_actions():
			pass
