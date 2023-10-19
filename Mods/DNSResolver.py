import ModBuilder.ModBuilder as mb
import dns.resolver as dr


deps = '''
dnspython
'''


class Mod(mb.ModIface):
	def __init__(self):
		self.rhost = mb.OptTemplate.CommonNet.RHOST

	def run(self):
		records = (
			'A',
			'AAAA',
			'MX',
			'CNAME'
		)
		for record in records:
			try:
				answers = dr.query(self.rhost.value, record)
				for answser in answers:
					print(answser)
			except Exception as e:
				print(e)
