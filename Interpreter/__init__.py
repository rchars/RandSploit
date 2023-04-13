import Interpreter.state
import pathlib


state.ACTION_DIRS = [
	pathlib.Path(__file__).parent / pathlib.Path('Actions')
]
state.MOD_DIRS = [
	pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
]
