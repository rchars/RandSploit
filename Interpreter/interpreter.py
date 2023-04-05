import Interpreter.state as state
import traceback
import readline


class InterpreterCompleter:
	possible_completions = None

	# not finished yet
	# if splitted text is > 1 then create the non-failure
	def complete(self, text, index):
		# if self.possible_completions is None:
		# 	self.possible_completions = list()
		# 	for action_mod in state.STATE.iter_actions():
		# 		if action_mod.stem.startswith(text):
		# 			self.possible_completions.append(action_mod.stem)
		# try:
		# 	return self.possible_completions[index]
		# except IndexError:
		# 	self.possible_completions = None
		# 	return None
		if self.possible_completions is None:
			self.possible_completions = list()
			for action_mod in state.STATE.iter_actions():
				if action_mod.stem.startswith(text):
					self.possible_completions.append(action_mod.stem)
		tokens = text.split()
		if len(tokens) < 1:
			try:
				return self.possible_completions[index]
			except IndexError:
				self.possible_completions = None
				return None
		try:
			mod = state.STATE.get_action_mod(tokens[0])
			return mod.complete(tokens[1:])
		except Exception:
			pass

def start_interpreter():
	completer_instance = InterpreterCompleter()
	readline.parse_and_bind('tab: complete')
	readline.set_completer(completer_instance.complete)
	while not state.STATE.exit:
		line = input(state.STATE.prompt)
		tokens = line.split()
		if not tokens:
			continue
		for action_mod in state.STATE.iter_actions():
			if action_mod.stem == tokens[0]:
				try:
					state.STATE.get_module_by_path(action_mod).Action().execute(tokens[1:])
				except Exception:
					traceback.print_exc()
				finally:
					break
		else:
			print(f'No such command \'{tokens[0]}\'')
