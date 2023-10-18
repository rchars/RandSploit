# import Interpreter.StateUtils as su
# import Interpreter.state as state
# import tabulate


# def iter_sessions():
# 	for session_id, session_pack in state.BACKGROUND_MODS.items():
# 		yield session_id, session_pack.name, session_pack.session.is_alive()


# def execute():
# 	print(
# 		tabulate.tabulate(
# 			iter_sessions(),
# 			tablefmt=state.TABLEFMT,
# 			headers=(
# 				'id',
# 				'name',
# 				'running'
# 			)
# 		)
# 	)
