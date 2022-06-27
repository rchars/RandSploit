__DEFAULT_REGISTERS_TABLE = {
	'name': [],
	'value': [],
	'description': [],
	'validator': []
}
REGISTERS_TABLE = __DEFAULT_REGISTERS_TABLE


# Look s horrrible, I ll refactor this later
def add_reg(name='', value='', description='', validator=None):
	REGISTERS_TABLE['name'] = name
	REGISTERS_TABLE['value'] = value
	REGISTERS_TABLE['description'] = description
	REGISTERS_TABLE['validator'] = validator


def update_reg(reg_name, new_value=''):
	index = REGISTERS_TABLE['names'].index(reg_name)
	validator = REGISTERS_TABLE['validator'][index]
	if validator:
		validator(new_value)
	REGISTERS_TABLE['value'][index] = new_value


def clean_reg_table():
	REGISTERS_TABLE = __DEFAULT_REGISTERS_TABLE