# import collections as c


# class SessionDict(c.UserDict):
# 	def __init__(self):
# 		super().__init__()
# 		self._tha_counter = 0
# 		self._session_pack = c.namedtuple(
# 			'SessionPack',
# 			[
# 				'session',
# 				'name'
# 			],
# 			defaults=(None,)
# 		)

# 	@property
# 	def session_pack(self):
# 		return self._session_pack

# 	def append(self, session):
# 		super().__setitem__(
# 			self._tha_counter,
# 			self._session_pack(
# 				session
# 			)
# 		)
# 		self._tha_counter += 1

# 	def __setitem__(self, key, value):
# 		raise TypeError('Cannot add values directly to this dictionary')
