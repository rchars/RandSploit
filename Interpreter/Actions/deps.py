import Interpreter.state as state
import ast


def install_deps(docstring):
	import pip._internal.cli.main as mn
	for dep in docstring.splitlines():
		if not dep: continue
		try:
			mn.main(['install', dep])
		except Exception as install_err:
			print(install_err)


def execute(mod_id):
	if not mod_id:
		if not state.MOD_HANDLER.is_mod_set():
			raise ValueError('deps <mod index or mod path>')
		mod_id = str(state.MOD_HANDLER.active_mod_path)
	elif mod_id.isdigit():
		deps_mod_index = int(mod_id)
		for mod_index, mod_path in state.MOD_HANDLER.iter_mods_with_index():
			if mod_index == deps_mod_index:
				mod_id = str(mod_path)
				break
		else: raise ValueError(f'No module has index \'{mod_id}\' assigned')
	with open(mod_id, 'r') as f:
		source_code = f.read()
	code = ast.parse(source_code)
	for node in ast.walk(code):
		if not isinstance(node, ast.Assign): continue
		for target in node.targets:
			if isinstance(target, ast.Name) and target.id == 'deps':
				if isinstance(node.value, ast.Str):
					docstring = node.value.s
					break
				elif isinstance(node.value, ast.Expr) and isinstance(node.value.value, ast.Str):
					docstring = node.value.value.s
					break
		else: continue
		break
	else: raise RuntimeError(f'The module \'{mod_id}\' has no external dependencies')
	install_deps(docstring)