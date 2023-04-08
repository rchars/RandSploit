import OptionInterface.OptionInterface as opt_iface
import Interpreter.ActionInterface as ai
import Interpreter.state as state
import tabulate
import inspect


class Action(ai.ActionInterface):
	# ugly
	def generate_table(self, params):
		for obj in vars(state.STATE.active_mod).values():
			if not isinstance(obj, opt_iface.OptionInterface):
				continue
			row = vars(obj)
			for key in row.items():
				if key not in params:
					del row[key]
			yield row

	def execute(self):
		if not state.STATE.is_mod_selected():
			print('Choose mod fist')
		else:
			iface_params = list(inspect.signature(opt_iface.OptionInterface).parameters.keys())
			tabulate.tabulate(self.generate_table(iface_params), headers=iface_params, tablefmt='fancy_grid')
