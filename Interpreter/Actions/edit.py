import Interpreter.SharedCompleters as ss
import Interpreter.Impl.ArgParser as ap
import Interpreter.state as state
import subprocess
import tempfile
import os


parser = ap.Parser()
parser.add_argument(
	'option'
)
parser.add_argument(
	'-e',
	action='store_true'
)
parser.add_argument(
	'--choose-editor',
	action='store_true'
)


def execute(text):
	'''Change the option's value in the text editor.'''
	if not state.MOD_HANDLER.is_mod_set():
		raise RuntimeError('Choose mod first')
	args = parser.parse_args(text)
	opt = state.MOD_HANDLER.get_mod_opt(args.option)
	current_opt_value = opt.value
	if args.e: current_opt_value = ''
	if not (editor_str := state.EDITOR_HANDLER.current_editor) or args.choose_editor:
		editor_str = input('Editor:')
	try:
		with tempfile.NamedTemporaryFile(mode='w', delete=False) as tf:
			tf.write(current_opt_value)
		proc = subprocess.run([editor_str, tf.name])
		if proc.returncode == 0:
			state.EDITOR_HANDLER.current_editor = editor_str
		with open(tf.name, 'r') as rtf:
				opt.value = rtf.read()
	finally: os.remove(tf.name)


complete = ss.complete
