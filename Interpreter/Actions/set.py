import Interpreter.Impl.ArgParser as ap
import Interpreter.state as state


# TODO:
# Replace "error" print statements with "RuntimeException".


parser = ap.Parser()
parser.add_argument('-e', '--editor')
parser.add_argument('option')
parser.add_argument('value')


def execute(text):
	'''Set an option for the chosen module'''
	if not state.MOD_HANDLER.is_mod_set():
		raise RuntimeError('Choose mod first')
	args = parser.parse_args(text)
	# if args.editor: pass
	state.MOD_HANDLER.set_mod_opt(
		name=args.option,
		value=args.value
	)


def complete(text):
	if not state.MOD_HANDLER.is_mod_set(): return
	completions = list()
	for params in state.MOD_HANDLER.iter_mod_opts_data():
		if params.name.startswith(text):
			completions.append(params.name)
	return completions
