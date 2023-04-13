import OptionInterface.OptionInterface as opt_iface
import importlib.machinery as mach
import Interpreter.state as state
import collections
import pathlib
import inspect


OptIfaceParams = list(inspect.signature(opt_iface.OptionInterface).parameters)
OptFields = collections.namedtuple('OptFields', OptIfaceParams)
OPT_IFACE_PARAMS = OptFields(*OptIfaceParams)


def get_params_count(func):
	return len(inspect.signature(func).parameters)


def call_func(func, arg):
	params_count = get_params_count(func)
	if params_count >= 1:
		return func(arg)
	else:
		return func()


def get_mod_inst(mod_path):
	return mach.SourceFileLoader(mod_path.name, str(mod_path)).load_module().Mod()


def get_mod_path(mod_stem):
	for mod_dir in state.MOD_DIRS:
		check_path = mod_dir / pathlib.Path(mod_stem)
		if check_path.is_file():
			return check_path
	else:
		raise FileNotFoundError(f'No such module as \'{mod_stem}\'')


def iter_mod_opts(mod_inst):
	for obj in vars(mod_inst).values():
		if not isinstance(obj, opt_iface.OptionInterface):
			continue
		yield obj


def iter_mod_opts_data(mod_inst):
	for opt in iter_mod_opts(mod_inst):
		fields = list()
		for param in OPT_IFACE_PARAMS:
			fields.append(getattr(opt, param))
		yield OptFields(*fields)
