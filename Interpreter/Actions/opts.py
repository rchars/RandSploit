import Interpreter.ActionInterface as ai
import Interpreter.state as state
import tabulate


class Action(ai.ActionInterface):
	# def generate_table(self, params):
	# 	for obj in vars(state.STATE.active_mod).values():
	# 		if not isinstance(obj, opt_iface.OptionInterface):
	# 			continue
	# 		row = list()
	# 		fields = vars(obj)
	# 		for param in params:
	# 			row.append(fields[param])
	# 		yield row

	def execute(self):
		if not state.STATE.is_mod_selected():
			print('Choose mod fist')
		else:
			# print(tabulate.tabulate(self.generate_table(iface_params), headers=iface_params, tablefmt=state.STATE.tablefmt))
			print(
				tabulate.tabulate(state.MOD_STATE.iter_mods_opts(), showindex='always', headers=state.MOD_STATE._opt_iface_params)
			)
