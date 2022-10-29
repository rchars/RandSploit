import randstate
import abc


class OptionIface(abc.ABC):
	def __init__(self, name, val, description, required=False):
		self.name = name
		self.val = val
		self.description = description
		self.required = required

	@abc.abstractmethod
	def validator(self, new_val):
		pass


class Option(OptionIface):
	def __init__(self, name, val='', description='', required=False):
		super().__init__(name, val, description, required)
	
	def validator(self, new_val): return str(new_val)


class CastOption(OptionIface):
	def __init__(self, name, val=None, description='', cast_to=int, required=True):
		if not callable(cast_to):
			raise TypeError('\'cast_to\' field must be callable')
		self.cast_to = cast_to
		if required not in (True, False):
			raise TypeError('\'required\' field must be True or False')
		self.val = val
		super().__init__(name, val, description, required=required)

	def validator(self, new_val):
		if not new_val and not self.required:
			return ''
		elif not new_val and self.required:
			raise ValueError('value cannot be empty')
		return self.cast_to(new_val)


class ModInterface(abc.ABC):
	def __init__(self, prompt=''):
		self.prompt = prompt

	@abc.abstractmethod
	def run(self):
		pass


def add_option(option):
	if not isinstance(option, OptionIface):
		raise TypeError('The option must be an instance of sublcass that inherits from Option')
	randstate.MOD_OPTIONS.append(option)


def get_option(option_name):
	for option in randstate.MOD_OPTIONS:
		if option_name == option.name:
			return option
	raise ValueError(f'No such option as \'{option_name}\'')


# check if 'required' field is True/False
# and then check if value is empty
def get_option_val(option_name):
	return get_option(option_name).val


def set_option_val(option_name, new_val):
	option = get_option(option_name)
	option.val = option.validator(new_val)


def check_required():
	options_not_set = []
	for option in randstate.MOD_OPTIONS:
		if option.required and not option.val:
			options_not_set.append(option.name)
	if options_not_set:
		raise ValueError('{} must be set'.format(','.join(options_not_set)))