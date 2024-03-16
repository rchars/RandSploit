import ModBuilder.ModBuilder as mb
import dns.resolver as dr
import ipaddress
import dns


deps = '''
dnspython
'''


class Mod(mb.ModIface):
	records = (
		'A',
		'AAAA',
		'MX',
		'CNAME'
	)

	def __init__(self):
		self.rhost = mb.OptTemplate.CommonNet.RHOST

	def to_ip(self):
		name = dr.resolve(dns.reversename.from_address(self.rhost.value), 'PTR')[0]
		print(name)

	def to_name(self):
		for record in self.records:
			try:
				answers = dr.query(self.rhost.value, record)
				for answser in answers:
					print(answser)
			except Exception as e:
				print(e)


	def run(self):
		try:
			ipaddress.ip_address(self.rhost.value)
		except ValueError: method = self.to_name
		else: method = self.to_ip
		method()
