import Interpreter.state as state
import Interpreter.Impl.SessionDict as isd
import pathlib


state.ACTION_DIRS = [
	pathlib.Path(__file__).parent / pathlib.Path('Actions')
]
state.MOD_DIRS = [
	pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
]
user_mods_path = pathlib.Path().home() / pathlib.Path('.RandSploit/Mods')
try:
	user_mods_path.mkdir(exist_ok=True, parents=True)
except OSError:
	pass
else:
	state.MOD_DIRS.append(user_mods_path)
state.BACKGROUND_MODS = isd.SessionDict()
