import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, tokens):
		state.STATE.exit = True
