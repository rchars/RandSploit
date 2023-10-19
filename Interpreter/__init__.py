import Interpreter.Impl.ModHandler as mh
import Interpreter.Impl.BoolGate as bg
import Interpreter.state as state
import pathlib


state.FRAME_DEV = bg.Gate(name='Frame developer')
state.MOD_DEV = bg.Gate(name='Module developer')
state.ACTION_DIRS = [
	pathlib.Path(__file__).parent / pathlib.Path('Actions')
]
mod_dirs = [pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')]
user_opt_templates_path = pathlib.Path().home() / pathlib.Path('.RandSploit/OptionTemplate')
user_opt_path = pathlib.Path().home() / pathlib.Path('.RandSploit/Actions')
user_mods_path = pathlib.Path().home() / pathlib.Path('.RandSploit/Mods')
user_util_path = pathlib.Path().home() / pathlib.Path('.RandSploit/Util')
user_editor = pathlib.Path().home() / pathlib.Path('RandSploit.editor')
if user_editor.is_file():
	with user_editor.open() as f:
		editor_str_path = f.readline()
	if editor_str_path != '':
		EDITOR = editor_str_path
try:
	user_opt_templates_path.mkdir(exist_ok=True, parents=True)
	user_mods_path.mkdir(exist_ok=True, parents=True)
	user_util_path.mkdir(exist_ok=True, parents=True)
	user_opt_path.mkdir(exist_ok=True, parents=True)
except OSError as e:
	pass
else:
	state.USER_OPT_TEMPLATE_DIR = user_opt_templates_path
	state.USER_UTIL_DIR = user_util_path
	state.USER_MOD_DIR = user_mods_path
	state.USER_OPT_DIR = user_opt_path
	mod_dirs.append(user_mods_path)
state.MOD_HANDLER = mh.Handler(
	mod_dirs
)
