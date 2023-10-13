# import Interpreter.Impl.SessionDict as isd
import Interpreter.Impl.ModHandler as mh
import Interpreter.Impl.BoolGate as bg
import Interpreter.state as state
import pathlib


state.MOD_DEV = bg.Gate(value=True, name='Module developer')
state.FRAME_DEV = bg.Gate(name='Frame developer')
# state.BACKGROUND_MODS = isd.SessionDict()
state.ACTION_DIRS = [
	pathlib.Path(__file__).parent / pathlib.Path('Actions')
]
# state.MOD_DIRS = [
# 	pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
# ]
mod_dirs = [pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')]
user_mods_path = pathlib.Path().home() / pathlib.Path('.RandSploit/Mods')
user_editor = pathlib.Path().home() / pathlib.Path('RandSploit.editor')
if user_editor.is_file():
	with user_editor.open() as f:
		editor_str_path = f.readline()
	if editor_str_path != '':
		EDITOR = editor_str_path
try:
	user_mods_path.mkdir(exist_ok=True, parents=True)
except OSError:
	pass
else:
	# state.MOD_DIRS.append(user_mods_path)
	mod_dirs.append(user_mods_path)
state.MOD_HANDLER = mh.Handler(
	mod_dirs
)
