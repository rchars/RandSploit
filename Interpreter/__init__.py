import pathlib
import state


class State:
	def __init__(self):
		self.active_mod = None
		self.prompt = 'rand>'
		# try to use property
		self.mod_locations = [
			pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
		]
		self.action_locations = [
			pathlib.Path(__file__).parent / pathlib.Path('Actions')
		]
	# provide some methods for managing this fields


# if __name__ == '__main__' ???
state.STATE = State()
