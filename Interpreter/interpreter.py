import readline
import state


def load_actions():
	for location in state.STATE.mod_locations


def interpreter_complete(text, state):
	pass


def start_interpreter():
	readline.parse_and_bind('tab: complete')
	readline.set_completer(interpreter_complete)
	while True:
		# get prompt from state
		line = input(state.STATE.prompt)


if __name__ == '__main__':
	start_interpreter()
