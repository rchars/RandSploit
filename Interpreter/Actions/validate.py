import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, tokens):
		print('The tokens should be a group of regex and nothing more')

	def complete(self, tokens):
		pass
