class RegisterManager:
	names = []
	values = []
	validators = []
	descriptions = []
	data_len = 0
	reg_index = 0

	def add_register(self, name, validator=None, value=None, description=None):
		self.names.append(name)
		self.validators.append(validator)
		self.values.append(value)
		self.descriptions.append(description)

	def set_new_value(self, search_name, new_value):
		# napisz to jak trzeba
		for index in range(0, self.data_len):
			check_name = self.names[index]
			if check_name == search_name:
				# podnies wyjatek, jezeli wartosc
				# nie taka jak trzeba
				if self.validators[index]:
					self.validators[index](new_value)
				self.values[index] = new_value
				break
		else:
			raise ValueError

	def __iter__(self):
		return self

	def __next__(self):
		if self.index >= self.data_len:
			raise StopIteration
		self.reg_index += 1
		return self.names[self.reg_index], self.values[self.reg_index], self.descriptions[self.reg_index]
