import Interpreter.state as state
import collections
import traceback
import readline
import inspect



PREP_LINE = collections.namedtuple('PrepLine', ['action_name', 'text'])


def prepare_line(text):
	text = text.lstrip()
	try:
		space_index = text.index(' ')
		action_mod_stem = text[0:space_index]
		action_arg_text = text[space_index + 1:].lstrip()
	except ValueError:
		action_mod_stem = text
		action_arg_text = ''
	return PREP_LINE(action_mod_stem, action_arg_text)


class Completer:
	possible_completions = None
	possible_completions_len = None

	def complete(self, text, index):
		prep_line = prepare_line(text)
		action_mod_stem = prep_line.action_name
		action_completion_text = prep_line.text
		self.set_actions(action_mod_stem)
		try:
			if self.possible_completions_len == 1 and self.possible_completions[0] == action_mod_stem:
				try:
					action_mod_inst = state.STATE.get_action_mod().Action()
					arg_num = len(inspect.getfullargspec(action_mod_inst.complete).args)
					if arg_num >= 1:
						return action_mod_inst.comlete(action_completion_text)
					return action_mod_inst.complete()
				except InstanceError:
					pass
				except Exception:
					pass
				finally:
					return None
			else:
				return self.possible_completions[index]
		except IndexError:
			self.possible_completions = None
			return None

	def set_actions(self, action_mod_stem):
		if self.possible_completions is None:
			self.possible_completions = list()
			for action_mod in state.STATE.iter_actions():
				if action_mod.stem.startswith(action_mod_stem):
					self.possible_completions.append(action_mod.stem)


def start_interpreter():
	readline.parse_and_bind('tab: complete')
	readline.set_completer(Completer().complete)
	while not state.STATE.exit:
		line = input(state.STATE.prompt)
		prep_line = prepare_line(line)
		if not prep_line.action_name:
			continue
		for action_mod in state.STATE.iter_actions():
			if action_mod.stem == prep_line.action_name:
				try:
					using_action_inst = state.STATE.get_module_by_path(action_mod).Action()
					arg_num = len(inspect.getfullargspec(using_action_inst.complete).args)
					if arg_num >= 2:
						using_action_inst.execute(prep_line.text)
					else:
						using_action_inst.execute()
				except Exception:
					traceback.print_exc()
				finally:
					break
		else:
			print(f'No such command \'{prep_line.action_name}\'')
