import Interpreter.SharedCompleters as ss
import Interpreter.Impl.ArgParser as ap
import Interpreter.state as state
import argparse


parser = ap.Parser(
	script_name='set'
)
parser.add_argument(
	'option'
)
parser.add_argument(
	'value',
	nargs=argparse.REMAINDER,
	default=''
)


def execute(text):
	'''Set an option for the chosen module'''
	args = parser.parse_args(text)
	if not state.MOD_HANDLER.is_mod_set():
		raise RuntimeError('Choose mod first')
	state.MOD_HANDLER.set_mod_opt(
		name=args.option,
		value=(
			value := ' '.join(args.value)
		)
	)
	print(f'{args.option} => {value}')


complete = ss.complete
