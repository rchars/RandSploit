import OptionInterface.OptionInterface as opt_iface
import Interpreter.ActionInterface as ai
import Interpreter.state as state
import inspect


class Action(ai.ActionInterface):
	def execute(self, text):
		if not state.STATE.is_mod_selected():
			print('select module first')
			return None
		tokens = text.split()
		tokens_len = len(tokens)
		if tokens_len == 0:
			print('set <opt name> <value>')
		elif tokens_len == 1:
			print('Need value')
		else:
			for obj in vars(state.STATE.active_mod).values():
				if not isinstance(obj, opt_iface.OptionInterface):
					continue
				elif obj.name == tokens[0]:
					new_value = ' '.join(tokens[1:])
					obj.value = new_value
					print(f'{tokens[0]} => {new_value}')
					break
			else:
				print(f'No such option as \'{tokens[0]}\'')

	def complete(self, text):
		if not state.STATE.is_mod_selected():
			return None
		completions = list()
		for obj in vars(state.STATE.active_mod).values():
			if not isinstance(obj, opt_iface.OptionInterface):
				continue
			# hardcoded == bad
			if obj.name.startswith(text):
				completions.append(obj.name)
		return completions
