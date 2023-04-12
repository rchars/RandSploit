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
	completions = None
	fulltext = ''

	def complete(self, text, index):
		if self.completions == None:
			prep_line = prepare_line(readline.get_line_buffer())
			self.set_actions(prep_line.action_name)
			if len(self.completions) == 1 and self.completions[0] == prep_line.action_name:
				self.completions = state.ACTION_STATE.call_action_completer(prep_line.action_name, prep_line.action_arg_text)
		try:
			return self.completions[index]
		except(IndexError, TypeError):
			self.completions = None
			return None

	def set_actions(self, action_mod_stem):
		self.completions = list()
		for action_mod in state.STATE.iter_actions():
			if action_mod.stem.startswith(action_mod_stem):
				self.completions.append(action_mod.stem)


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
					arg_num = len(inspect.signature(using_action_inst.execute).parameters)
					if arg_num >= 1:
						using_action_inst.execute(prep_line.text)
					else:
						using_action_inst.execute()
				except Exception:
					traceback.print_exc()
				finally:
					break
		else:
			print(f'No such command \'{prep_line.action_name}\'')
