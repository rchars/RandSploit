import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self, text):
		if not text:
			print('Use what ?')
		else:
			try:
				mod_id = int(text)
			except ValueError:
				# regex
				mod_id = text
			state.MOD_STATE.active_mod = mod_id

	def complete(self, text):
		pass
