import OptionInterface.OptionInterface as opt_iface
import Interpreter.Impl.Session as sn
import importlib.machinery as mach
import Interpreter.state as state
import importlib.util as iu
import dataclasses as ds
import collections
import pathlib
import inspect
import copy
import enum
import sys


# Bloat
OptIfaceParams = list(inspect.signature(opt_iface.OptionInterface).parameters)
OptFields = collections.namedtuple('OptFields', OptIfaceParams)
OPT_IFACE_PARAMS = OptFields(*OptIfaceParams)


class CommonExc(enum.Enum):
	@ds.dataclass
	class exc:
		exc: None
		msg: str

		def __post_init__(self):
			if not issubclass(self.exc, Exception):
				raise TypeError('exc must be exception')
			if type(self.msg) != str:
				raise TypeError('msg must be str')

	MOD_NF = exc(exc=ModuleNotFoundError, msg='No such module as \'{}\'')
	ACTION_NF = exc(exc=ModuleNotFoundError, msg='No such command as \'{}\'')

	@classmethod
	def get_exc(cls, exc, *strings):
		using_exc = cls[exc.name].value
		if strings:
			return using_exc.exc(using_exc.msg.format(*strings))
		return using_exc.exc(using_exc.msg)


def get_params_count(func):
	return len(inspect.signature(func).parameters)


def call_func(func, arg):
	params_count = get_params_count(func)
	if params_count >= 1:
		return func(arg)
	else:
		return func()


def get_mod_inst(mod_path):
	relative_path = f'{mod_path.parent.name}.{mod_path.stem}'
	spec = mach.ModuleSpec(
		name=relative_path,
		loader=mach.SourceFileLoader(relative_path, str(mod_path)),
		origin=mod_path,
		is_package=False
	)
	mod = iu.module_from_spec(spec)
	spec.loader.exec_module(mod)
	sys.modules[relative_path] = mod
	return mod.Mod()


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


def reload_current_mod():
	active_mod_copy = copy.deepcopy(state.ACTIVE_MOD)
	state.ACTIVE_MOD = active_mod_copy
	state.ACTIVE_MOD_PROC = sn.Session(active_mod_copy)
	# No need to reload the prompt, cuz it will be here already


def unset_current_mod():
	state.ACTIVE_MOD_PROC = None
	state.ACTIVE_MOD = None
	state.PROMPT = 'rand>'
