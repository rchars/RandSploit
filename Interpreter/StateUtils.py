import OptionInterface.OptionInterface as opt_iface
import importlib.machinery as mach
import Interpreter.state as state
import dataclasses as ds
import collections
import pathlib
import inspect
import enum


OptIfaceParams = list(inspect.signature(opt_iface.OptionInterface).parameters)
OptFields = collections.namedtuple('OptFields', OptIfaceParams)
OPT_IFACE_PARAMS = OptFields(*OptIfaceParams)


# finish this class
class CommonExc(enum.Enum):
	@ds.dataclass
	class CommonExc:
		exc: None
		msg: str

		def __post_init__(self):
			if not issubclass(self.exc, Exception):
				raise TypeError('exc must be exception')
			if type(self.msg) != str:
				raise TypeError('msg must be str')

	MOD_NF = CommonExc(exc=FileNotFoundError, msg='')
	ACTION_NF = CommonExc(exc=FileNotFoundError, msg='')

	@classmethod
	def get_exc(self, exc, *strings):
		pass


def format_common_exc(exc, *strings):
	pass


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
