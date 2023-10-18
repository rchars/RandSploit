import os


def execute(command):
	'''Call an OS command.'''
	if not command or 'help'.startswith(command.lower()):
		print('call <command>')
	os.system(command)