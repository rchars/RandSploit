import Interpreter.StateUtils as su
import importlib.machinery as mach
import Interpreter.state as state
import collections
import traceback
import readline
import inspect


PREP_LINE = collections.namedtuple('PrepLine', ['action_name', 'text'])


def get_action_inst(action_stem):
	for action_dir in state.ACTION_DIRS:
		for action_path in action_dir.iterdir():
			if action_path.stem == action_stem:
				return mach.SourceFileLoader(action_path.name, str(action_path)).load_module()
	else:
		raise FileNotFoundError(f'No such command as \'{action_stem}\'')


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
				self.completions = self.call_action_completer(prep_line.action_name, prep_line.text)

		try:
			return self.completions[index]
		except(IndexError, TypeError):
			self.completions = None
			return None

	def set_actions(self, action_mod_stem):
		self.completions = list()
		for action_dir in state.ACTION_DIRS:
			for action_mod in action_dir.iterdir():
				if action_mod.stem.startswith(action_mod_stem):
					self.completions.append(action_mod.stem)

	def call_action_completer(self, action_stem, compl_text):
		using_func = get_action_inst(action_stem).complete
		arg_num = su.get_params_count(
			using_func
		)
		if arg_num >= 1:
			return using_func(compl_text)
		else:
			return using_func()


def start_interpreter():
	readline.parse_and_bind('tab: complete')
	readline.set_completer(Completer().complete)
	while not state.END:
		line = input(state.PROMPT)
		prep_line = prepare_line(line)
		if not prep_line.action_name:
			continue
		try:
			using_action_inst = get_action_inst(prep_line.action_name)
			arg_num = su.get_params_count(using_action_inst.execute)
			if arg_num >= 1:
				using_action_inst.execute(prep_line.text)
			else:
				using_action_inst.execute()
		except Exception:
			traceback.print_exc()
