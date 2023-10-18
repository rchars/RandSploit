import Option.ValidatedOpt as v_opt
import Option.DefaultOpt as d_opt


RHOST = d_opt.Opt(name='RHOST', value='localhost')
LHOST = d_opt.Opt(name='LHOST', value='localhost')


def port_validator(new_value):
	if not new_value.isdigit():
		raise ValueError('Port must be a number in range of 1 to 65535')
	new_value = int(new_value)
	if not (1 <= new_value <= 65535):
		raise ValueError('Port must be a number in range of 1 to 65535')
	return new_value


RPORT = v_opt.Opt(name='RPORT', validator=port_validator)
LPORT = v_opt.Opt(name='LPORT', validator=port_validator)
