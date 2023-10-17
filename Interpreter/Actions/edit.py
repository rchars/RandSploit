import Interpreter.state as state
import os


def call_editor(mod_str_path):
	if mod_str_path.isdigit():
		mod_index = int(mod_str_path)
		for index, mod_path in state.MOD_HANDLER.iter_mods_with_index():
			if index == mod_index:
				mod_str_path = str(mod_path)
				break
		else: raise ValueError('No module has index \'{mod_index}\' assigned')
	if not state.EDITOR:
		using_editor = input('Editor:')
	else: using_editor = state.EDITOR
	os.system(f'{using_editor} {mod_str_path}')


def execute(module):
	if module: call_editor(module)
	elif state.MOD_HANDLER.is_mod_set():
		call_editor(state.MOD_HANDLER.active_mod_path)
	else: print('Choose a module first.')
