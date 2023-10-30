import argparse


class Parser(argparse.ArgumentParser):
	def __init__(self, script_name='', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._script_name = script_name

	script_name = property(lambda self: self._script_name)

	def format_help(self):
		return super().format_help().replace(
			'usage: randconsole.py',
			f'usage: {self._script_name}'
		)

	def parse_args(self, args, namespace=None):
		if isinstance(args, str):
			prepared_args = args.split()
		else:
			prepared_args = args
		return super().parse_args(prepared_args, namespace)
