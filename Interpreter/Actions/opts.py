import Interpreter.ActionInterface as ai
import Interpreter.state as state
import tabulate


class Action(ai.ActionInterface):
	def execute(self):
		if not state.STATE.is_mod_selected():
			print('Choose mod fist')
		else:
			# print(tabulate.tabulate(self.generate_table(iface_params), headers=iface_params, tablefmt=state.STATE.tablefmt))
			print(
				tabulate.tabulate(state.MOD_STATE.iter_mods_opts(), showindex='always', headers=state.MOD_STATE._opt_iface_params)
			)
