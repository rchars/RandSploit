import abc


class ActionInterface(abc.ABC):
	@abc.abstractmethod
	def execute():
		pass

	# may be empty
	def complete(text):
		pass
