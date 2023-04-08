import Interpreter.ActionInterface as ai
import Interpreter.state as state


class Action(ai.ActionInterface):
	def execute(self):
		if not state.STATE.is_mod_selected():
			print('Select mod before executing')
		else:
			state.STATE.active_mod.run()
