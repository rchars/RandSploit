import argparse


class Parser(argparse.ArgumentParser):
	def error(self, msg):
		print(f'Error: {msg}')
		self.print_help()

	def parse_args(self, args, namespace=None):
		if isinstance(args, str):
			prepared_args = args.split()
		else:
			prepared_args = args
		return super().parse_args(prepared_args, namespace)