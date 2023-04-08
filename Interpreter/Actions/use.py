import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, text):
		if not text:
			print('Use what ?')
		else:
			state.STATE.active_mod = state.STATE.get_module_by_id(text)

	def complete(self, text):
		pass
