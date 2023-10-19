import Option.ValidatedOpt as v_opt
import Option.DefaultOpt as d_opt


RHOST = d_opt.Opt(name='RHOST', value='localhost')
LHOST = d_opt.Opt(name='LHOST', value='localhost')


def port_validator(new_value):
	if not new_value.isdigit():
		raise ValueError('Port must be a integer in range of 1 to 65535')
	new_value = int(new_value)
	if not (1 <= new_value <= 65535):
		raise ValueError('Port must be a integer in range of 1 to 65535')
	return new_value


RPORT = v_opt.Opt(name='RPORT', validator=port_validator)
LPORT = v_opt.Opt(name='LPORT', validator=port_validator)


def cli_limit_validator(new_value):
	err = ValueError('Client limit must be a positive integer')
	if isinstance(new_value, str):
		if not new_value.isdigit(): raise err
		new_value = int(new_value)
	elif not isinstance(new_value, int): raise err
	if new_value <= 0: raise err
	return new_value


CLI_LIMIT = v_opt.Opt(name='CLI_LIMIT', value=3, validator=cli_limit_validator, required=False)
