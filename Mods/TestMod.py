import ModInterface.ModInterface as mod_iface
import Option.Option as opt


class Mod(mod_iface.ModInterface):
	def __init__(self):
		self.a = opt.DefaultOpt('x', 'y', 'z')
		self.b = opt.ValidatedOpt('q', 'd', 'p')

	def run(self):
		print(self.a.name)
		print(self.b.value)
