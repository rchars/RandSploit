import pathlib
import pyclbr

p = pathlib.Path('RandMods/test.py')
name = p.name
package = p.parent
x = [str(package), name]
validate_module = pyclbr.readmodule_ex('test', path=x)
for key, val in validate_module.items():
	print(f'{key}: {val} - {val.name}')
	if isinstance(validate_module[key], pyclbr.Function):
		print('valid')


print(validate_module)
