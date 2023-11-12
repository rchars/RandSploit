import Interpreter.Impl.ArgParser as ap
import Interpreter.state as state
import subprocess
import os


parser = ap.Parser(
	script_name='emod'
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('module', nargs='?')
group.add_argument('--current', action='store_true')


def execute(text):
	args = parser.parse_args(text)
	search_by = 1
	if args.current:
		if not state.MOD_HANDLER.is_mod_set():
			raise RuntimeError('Choose mod first')
		mod_id = state.MOD_HANDLER.active_mod_path
	else:
		if args.module.isdigit():
			mod_id = int(args.module)
			search_by = 0
		else: mod_id =  args.module
	editor_str = state.EDITOR_HANDLER.ask_for_editor()
	for pack in state.MOD_HANDLER.iter_mods_with_index():
		if pack[search_by] == mod_id:
			subprocess.run(
				[editor_str, str(pack[1])]
			)
			break
	else: raise ModuleNotFoundError(f'No such module as \'{mod_id}\'')
