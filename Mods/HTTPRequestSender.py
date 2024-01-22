import ModBuilder.ModBuilder as mb
import requests
import json


deps = '''
requests
'''


methods_impl = {
	'GET': requests.get,
	'POST': requests.post,
	'DELETE': requests.delete,
	'HEAD': requests.head,
	'OPTIONS': requests.options,
	'PUT': requests.put
}


def validate_methods(method):
	if method not in methods_impl.keys():
		raise ValueError(f'No such method as \'{method}\'')
	return method


class Mod(mb.ModIface):
	def __init__(self):
		self.url = mb.Opt.DefaultOpt(name='URL')
		self.method = mb.Opt.ValidatedOpt(
			validator=validate_methods,
			name='METHOD',
			value='GET'
		)
		self.data = mb.Opt.DefaultOpt(
			required=False,
			name='DATA'
		)
		self.json = mb.Opt.DefaultOpt(
			required=False,
			name='JSON'
		)

	def run(self):
		using_json = ''
		if self.json.value != '':
			try:
				using_json = json.loads(self.json.value)
			except json.JSONDecodeError as e:
				print(e)
				return
		r = methods_impl[
			self.method.value
		](
			url=self.url.value,
			data=self.data.value,
			json=using_json
		)
		print(r.status_code, r.text)
